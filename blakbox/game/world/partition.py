from blakbox.globs import pg

# TODO: this class could handle scene serialization to JSON \(OoO)/
# ------------------------------------------------------------ #
class StaticPartition:
    def __init__(self, size: list[int], cellsize: int) -> None:
        self.objs = []
        self.size = size                                                # in cells
        self.width = size[0]                                            # in cells
        self.height = size[1]                                           # in cells
        self.cellsize = cellsize                                       # in pixels
        self.cells = [[] for _ in range(self.width * self.height)]

    def get_cell(self, pos: list[int]) -> list:
        """Returns all objects at the given world (pixel) position."""
        gx = int(pos[0]) // self.cellsize
        gy = int(pos[1]) // self.cellsize
        if gx < 0 or gy < 0 or gx > self.size[0] or gy > self.size[1]: return
        index = gy * self.width + gx
        if index >= len(self.cells): return
        return self.cells[index]
    
    def set_cell(self, obj) -> None:
        """Places an object in the grid at the given world (pixel) position."""
        if isinstance(obj, list):
            for o in obj:
                if o is None: continue
                cell = self.get_cell(o.pos)
                if cell is None or o in cell: return
                self.objs.append(o)
                cell.append(o)
        else:
            cell = self.get_cell(obj.pos)
            if cell is None or obj in cell: return
            self.objs.append(obj)
            cell.append(obj)

    def rem_cell(self, obj) -> None:
        """Removes and an object from the grid at the given world (pixel) position."""
        cell = self.get_cell(obj.pos)
        if cell is None: return
        self.objs.remove(obj)
        cell.remove(obj)

    def _generate_region(self, size:list[int], pos:list[int]) -> list[list[int]]:
        center = [
            int(pos[0]) // self.cellsize,
            int(pos[1]) // self.cellsize
        ]; region = []
        for x in range(center[0] - size[0], (center[0] + size[0]) + 1):
            for y in range(center[1] - size[1], (center[1] + size[1]) + 1):
                region.append([x, y])
        return region
    
    def get_area(self, topleft:list[int], bottomright:list[int]) -> list[list[int]]:
        start = [
            int(topleft[0]) // self.cellsize,
            int(topleft[1]) // self.cellsize
        ]; end = [
            int(bottomright[0]) // self.cellsize,
            int(bottomright[1]) // self.cellsize
        ]; cells = []
        for x in range(start[0], end[0]):
            for y in range(start[1], end[1]):
                cell = self.cells[y * self.size[0] + x]
                if cell:
                    cells.append(cell)
        return [o for cell in cells for o in cell if cell]

    def get_region(self, size:list[int], pos:list[int]) -> list|None:
        region = self._generate_region(size, pos)
        if not region: return None
        cells = []
        for map_pos in region:
            index = map_pos[1] * self.size[0] + map_pos[0]
            if index >= len(self.cells): continue
            cell = self.cells[index]
            if cell: cells.append(cell)
        return cells

    def debug_render(self, renderer, center: list[int|float], radius: int=8) -> None:
        """Renders a portion of the grid around a center position within a given radius."""
        cell_w, cell_h = self.cellsize, self.cellsize
        radius_px = radius * cell_w  # convert radius from cells to pixels

        # convert world position to grid cell indices
        start_x = max((int(center[0]) - radius_px) // cell_w, 0)
        start_y = max((int(center[1]) - radius_px) // cell_h, 0)
        end_x = min((int(center[0]) + radius_px) // cell_w, self.size[0] - 1)
        end_y = min((int(center[1]) + radius_px) // cell_h, self.size[1] - 1)

        # draw grid lines within the region
        for gx in range(start_x, end_x):
            x = gx * cell_w
            renderer.window.draw_line([x, start_y * cell_h], [x, end_y * cell_h], color=[255, 255, 255], width=1)
        
        for gy in range(start_y, end_y):
            y = gy * cell_h
            renderer.window.draw_line([start_x * cell_w, y], [end_x * cell_w, y], color=[255, 255, 255], width=1)

        # draw objects within the visible region
        for obj in self.objs:
            x, y = obj.center
            gx = x // self.cellsize
            gy = y // self.cellsize
            if start_x <= gx <= end_x and start_y <= gy <= end_y:
                obj_x, obj_y = gx * cell_w, gy * cell_h
                renderer.window.draw_circle(self.cellsize, [obj_x + self.cellsize / 2, obj_y + self.cellsize / 2], color=[0, 255, 0], width=1)
# ------------------------------------------------------------ #