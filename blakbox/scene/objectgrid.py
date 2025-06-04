from blakbox.atom import BOXatom
from blakbox.utils import div2_v2i, div_v2
from blakbox.resource.object import BOXobject

# ------------------------------------------------------------ #
class BOXobjectgrid(BOXatom):
    def __init__(
            self,
            cell_size: list[int],
            grid_size: list[int]
        ) -> None:
        super().__init__(0, 0)
        self.all = []
        self.grid_width: int = grid_size[0]                                 # in cells
        self.grid_height: int = grid_size[1]                                # in cells
        self.grid_size: list[int] = grid_size                               # in cells
        self.grid_area: int = self.grid_width * self.grid_height            # in cells
        
        self.cell_width: int = cell_size[0]                             # in pixels
        self.cell_height: int = cell_size[1]                            # in pixels
        self.cell_size: list[int] = cell_size                           # in pixels
        self.cell_area: int = self.cell_width * self.cell_height        # in pixels

        self.grid: list = [[] for _ in range(self.grid_area)]

    def _gen_region(self, size:list[int], pos:list[int]) -> list[list[int]]:
        region = []
        cx, cy = map(int, div2_v2i(pos, self.cell_size))
        for x in range(cx - size[0], (cx + size[0]) + 1):
            for y in range(cy - size[1], (cy + size[1]) + 1):
                region.append([x, y])
        return region

    def world_to_cell(self, pos: list[float]) -> list[int]:
        gx, gy = map(int, div_v2(pos, self.cell_width))
        if gx < 0 or gy < 0 or gx > self.grid_width or gy > self.grid_height:
            return None
        else: return [gx, gy]

    def cell_to_world(self, cell: list[int]) -> list[int]:
        return [cell[0] * self.cell_width, cell[1] * self.cell_height]

    def get(self, pos: list[float]) -> list:
        grid_pos = self.world_to_cell(pos)
        if grid_pos is None: return
        
        index = grid_pos[1] * self.grid_width + grid_pos[0]
        if index < 0 or index >= self.grid_area: return

        return self.grid[index]
    
    def rem(self, object: BOXobject, pos: list[float] = None) -> None:
        cell = self.get(object.pos if pos is None else pos)
        if cell is None or object not in cell: return
        
        cell.remove(object)
        if object in self.all:
            self.all.remove(object)
    
    def set(self, object: BOXobject, pos: list[float] = None) -> None:
        cell = self.get(object.pos if pos is None else pos)
        if cell is None or object in cell: return
        
        cell.append(object)
        if object not in self.all:
            self.all.append(object)

    def setv(self, objects: list[BOXobject]) -> None:
        if not isinstance(objects, list): return
        for object in objects:
            if not object: continue

            cell = self.get(object.pos)
            if cell is None or object in cell or object in self.all: continue
            
            cell.append(object)
            self.all.append(object)

    def set_region(self, size: list[int], pos: list[int], object: BOXobject) -> None: pass
    
    def get_region(self, size: list[int], pos: list[int]) -> list[BOXobject]:
        region = self._gen_region(size, pos)
        if not region: return None

        cells = []
        for gx, gy in region:
            index = gy * self.grid_width + gx
            if index < 0 or index >= self.grid_area: continue
            cell = self.grid[index]
            if cell: cells.append(cell)
        return cells

    def rem_region(self, size: list[int], pos: list[int]) -> None:
        region = self._gen_region(size, pos)
        if not region: return None

        for gx, gy in region:
            index = gy * self.grid_width + gx
            if index < 0 or index >= self.grid_area: continue
            self.grid[index] = []

    def update(self) -> None:
        for object in self.all:
            object.grid_cell = self.world_to_cell(object.pos)
            if object.grid_cell != object._last_cell:
                if object._last_cell:
                    self.rem(object, self.cell_to_world(object._last_cell))
                self.set(object, object.pos)
                object._last_cell = object.grid_cell
# ------------------------------------------------------------ #
