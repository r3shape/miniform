from r3frame.objects.game import Game_Object

class Grid_Map:
    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.cells = {}
        self.width = width                                  # in cells
        self.height = height                                # in cells
        self.cell_size = cell_size                          # in pixels
        self.size = [width * cell_size, height * cell_size] # in pixels

    def get_cell(self, x: int, y: int) -> Game_Object | None:
        """Returns the object at the given world (pixel) position."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        gx, gy = x // self.cell_size, y // self.cell_size
        return self.cells.get((gx, gy), None)

    def set_cell(self, x: int, y: int, obj: Game_Object) -> None:
        """Places an object in the grid at the given world (pixel) position."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        if self.get_cell(x, y): return

        gx, gy = x // self.cell_size, y // self.cell_size
        obj.location = [gx * self.cell_size, gy * self.cell_size]
        self.cells[(gx, gy)] = obj
    
    def rem_cell(self, x: int, y: int) -> Game_Object|None:
        """Removes and returns an object from the grid at the given world (pixel) position."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        obj = self.get_cell(x, y)
        if obj is not None: 
            gx, gy = x // self.cell_size, y // self.cell_size
            del self.cells[(gx, gy)]
        return obj

    def get_region(self, x: int, y: int) -> dict[str, Game_Object | None]:
        """Gets the object in the given cell and its immediate neighbors."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        gx, gy = x // self.cell_size, y // self.cell_size
        directions = {
            "center": (0, 0),
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "left-up": (-1, -1),
            "right-up": (1, -1),
            "left-down": (-1, 1),
            "right-down": (1, 1),
        }
        return {dir_name: self.cells.get((gx + dx, gy + dy)) for dir_name, (dx, dy) in directions.items()}
    
    def query_region(self, x: int, y: int, radius: int = 1) -> dict[tuple[int, int], Game_Object | None]:
        """Returns objects in a region centered at (x, y) within the given radius.
        
        Arguments:
        - x, y: The world (pixel) position to search around.
        - radius: The search radius in number of cells.
        
        Returns:
        - A dictionary where keys are grid coordinates (gx, gy) and values are the objects in those cells.
        """
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: 
            return {}

        gx, gy = x // self.cell_size, y // self.cell_size
        region = {}

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell_x, cell_y = gx + dx, gy + dy
                if 0 <= cell_x < self.width and 0 <= cell_y < self.height:
                    region[(cell_x, cell_y)] = self.cells.get((cell_x, cell_y))

        return region

    def debug_render(self, renderer, center: list[int|float], radius: int=8):
        """Renders a portion of the grid around a center position within a given radius."""
        cell_w, cell_h = self.cell_size, self.cell_size
        radius_px = radius * cell_w  # convert radius from cells to pixels

        # convert world position to grid cell indices
        start_x = max((int(center[0]) - radius_px) // cell_w, 0)
        start_y = max((int(center[1]) - radius_px) // cell_h, 0)
        end_x = min((int(center[0]) + radius_px) // cell_w, self.width - 1)
        end_y = min((int(center[1]) + radius_px) // cell_h, self.height - 1)

        # draw grid lines within the region
        for gx in range(start_x, end_x + 1):
            x = gx * cell_w
            renderer.draw_line([x, start_y * cell_h], [x, (end_y + 1) * cell_h], [125, 125, 125], 1)
        
        for gy in range(start_y, end_y + 1):
            y = gy * cell_h
            renderer.draw_line([start_x * cell_w, y], [(end_x + 1) * cell_w, y], [125, 125, 125], 1)

        # draw objects within the visible region
        for (gx, gy), obj in self.cells.items():
            if start_x <= gx <= end_x and start_y <= gy <= end_y:
                obj_x, obj_y = gx * cell_w, gy * cell_h
                renderer.draw_circle([obj_x + self.cell_size / 2, obj_y + self.cell_size / 2], self.cell_size, [255, 255, 255], 1)
