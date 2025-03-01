from r3frame.objects.game import Game_Object

class Quad_Cell:
    def __init__(self, x: int, y: int, width: int, height: int, depth: int=0, depth_max: int=10, object_max: int=64) -> None:
        self.bounds = [x, y, width, height]
        self.objects = []
        self.children = None  # will hold 4 Quad_Cell objects after subdivision
        self.depth = depth
        self.depth_max = depth_max
        self.object_max = object_max

    def subdivide(self):
        """Splits the cell into four equal-sized children."""
        x, y, size, _ = self.bounds
        half = size / 2

        self.children = [
            Quad_Cell(x, y, half, half, self.depth + 1, depth_max=self.depth_max, object_max=self.object_max),         # Top-left
            Quad_Cell(x + half, y, half, half, self.depth + 1, depth_max=self.depth_max, object_max=self.object_max),  # Top-right
            Quad_Cell(x, y + half, half, half, self.depth + 1, depth_max=self.depth_max, object_max=self.object_max),  # Bottom-left
            Quad_Cell(x + half, y + half, half, half, self.depth + 1, depth_max=self.depth_max, object_max=self.object_max),  # Bottom-right
        ]

        # reassign objects to children
        for obj in self.objects:
            self.insert(obj)
        self.objects.clear()  # clear from parent after distributing

    def insert(self, obj: Game_Object):
        """Inserts an object into the cell or its children."""
        x, y, size, _ = self.bounds

        # if this cell has children, forward the object to the correct cell
        if self.children:
            for child in self.children:
                if child.contains(obj.location):
                    child.insert(obj)
                    return

        # otherwise, store the object here
        self.objects.append(obj)

        # if too many objects, subdivide
        if len(self.objects) >= self.object_max and self.depth < self.depth_max:
            if not self.children: self.subdivide()

    def contains(self, location: list[int|float]):
        """Checks if a position is inside this cell's bounds."""
        x, y, size, _ = self.bounds
        px, py = location
        return x <= px < x + size and y <= py < y + size

    def get(self, x, y):
        """Retrieves the object at a given position."""
        if not self.contains((x, y)):
            return None

        if self.children:
            for child in self.children:
                result = child.get(x, y)
                if result:
                    return result

        for obj in self.objects:
            if obj.location == [x, y]:
                return obj
        return None

class Quad_Map:
    def __init__(self, width: int, height: int, cell_size: int, depth_max: int=10, object_max: int=64) -> None:
        self.objects = []                                   # an unordered list containing every object in the quadmap (used for quick loops but not for specific retrieval).
        self.width = width                                  # in cells
        self.height = height                                # in cells
        self.cell_size = cell_size                          # in pixels
        self.size = [width * cell_size, height * cell_size] # in pixels
        self.root = Quad_Cell(0, 0, *self.size, 0, depth_max=depth_max, object_max=object_max)  # Root covers entire world

    def set_cell(self, x: int, y: int, obj: Game_Object) -> None:
        """Places an object in the grid at the given world (pixel) position."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        
        gx, gy = x // self.cell_size, y // self.cell_size
        obj.location = [gx * self.cell_size, gy * self.cell_size]
        
        self.root.insert(obj)
        self.objects.append(obj)

    def get_cell(self, x: int, y: int) -> Game_Object | None:
        """Returns the object at the given world (pixel) position."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        return self.root.get(x, y)

    def get_region(self, x: int, y: int) -> list[Game_Object]:
        """Gets the object in the given cell and its immediate neighbors."""
        if x < 0 or x >= self.size[0] or y < 0 or y >= self.size[1]: return
        results = []
        self.query_region(self.root, x, y, self.cell_size, results)
        return results

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

        def _query(cell: Quad_Cell):
            """Recursively searches the quadtree for objects within the given radius."""
            if cell is None:
                return

            cx, cy, size, _ = cell.bounds

            # if the cell is completely outside the query region, ignore it
            if cx + size < (gx - radius) * self.cell_size or cx > (gx + radius) * self.cell_size or \
            cy + size < (gy - radius) * self.cell_size or cy > (gy + radius) * self.cell_size:
                return

            # if the cell has children, search deeper
            if cell.children:
                for child in cell.children:
                    _query(child)
            else:
                # collect objects within the search radius
                for obj in cell.objects:
                    obj_gx, obj_gy = obj.location[0] // self.cell_size, obj.location[1] // self.cell_size
                    if abs(obj_gx - gx) <= radius and abs(obj_gy - gy) <= radius:
                        region[(obj_gx, obj_gy)] = obj

        _query(self.root)
        return region

    def render_debug(self, renderer):
        """Visualizes the quadtree by drawing its regions."""
        self._draw_cell(self.root, renderer)

    def _draw_cell(self, cell, renderer):
        """Recursively draw each cell in a quadtree."""
        if not cell: return
        
        # draw the bounding box of this cell
        x, y, w, h = cell.bounds
        renderer.draw_rect([w, h], [x, y], [125, 125, 125], 1)

        # draw objects inside this cell as simple circles
        for obj in cell.objects:
            renderer.draw_circle([obj.location[0] + obj.size[0]/2, obj.location[1] + obj.size[1]/2], self.cell_size, [255, 255, 255], 1)

        # recurse into children if they exist
        if cell.children:
            for child in cell.children:
                self._draw_cell(child, renderer)
