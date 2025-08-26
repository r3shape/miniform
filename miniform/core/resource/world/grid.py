from miniform.imports import pg
import miniform

from .object import MiniStaticObject, MiniDynamicObject

class MiniGridPartition(miniform.MiniAtom):
    def __init__(
            self,
            
            app: "miniform.app.MiniApp",
            world: "miniform.resource.Hworld",

            cell_size: list[int],
            cell_origin: list[int] = [0, 0]
    ) -> None:
        super().__init__()
        self.cache: miniform.resource.MiniCache = app.cache
        self.world: miniform.resource.world.Miniworld = world

        self.cell_origin: list[int] = [*map(int, cell_origin)]

        self.cell_width: int = int(cell_size[0])
        self.cell_height: int = int(cell_size[1])
        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_area: int = self.cell_size[0] * self.cell_size[1]

        self.loaded_cells: set[tuple[int]] = set()
        self.cells: dict[tuple[int], set[MiniStaticObject|MiniDynamicObject]] = {}

    def get_cell_pos(self, pos: list[int | float]) -> tuple[int]:
        return tuple(miniform.utils.div2_v2i(miniform.utils.sub_v2(pos, self.cell_origin), self.cell_size))
    
    def get_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 0, ydir: int = 0) -> list[tuple[int]]:
        top_left = pos
        bottom_right = miniform.utils.sub_v2(miniform.utils.add_v2(pos, size), [1, 1])

        region = []
        grid_pos0 = miniform.utils.div2_v2i(top_left, self.cell_size)
        grid_pos1 = miniform.utils.div2_v2i(bottom_right, self.cell_size)
        for y in range(grid_pos0[1] - ydir, grid_pos1[1] + ydir + 1):
            for x in range(grid_pos0[0] - xdir, grid_pos1[0] + xdir + 1):
                region.append((x, y))
        return tuple(region)

    def load_cell(self, pos: list[int]) -> None:
        if pos in self.loaded_cells: return
        self.cells[pos] = set()
        self.loaded_cells.add(pos)

    def unload_cell(self, pos: list[int]) -> None:
        if pos not in self.loaded_cells: return
        del self.cells[pos]
        self.loaded_cells.remove(pos)

    def add_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        region = self.get_cell_region(obj.pos, obj.size)
        obj.spatial_index.clear()
        for cell_pos in region:
            if cell_pos not in self.loaded_cells:
                self.load_cell(cell_pos)

            cell = self.cells[cell_pos]
            if obj in cell: continue
            
            cell.add(obj)
            obj.spatial_index.add(cell_pos)

    def rem_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        for cell_pos in obj.spatial_index:
            cell = self.cells.get(cell_pos, None)
            if cell is None: continue

            if obj in cell:
                cell.remove(obj)

            if len(cell) == 0: self.unload_cell(cell_pos)
        obj.spatial_index.clear()

    def query_cell(self, pos: list[int | float]) -> set[MiniStaticObject|MiniDynamicObject] | set[None]:
        return self.cells.get(self.get_cell_pos(pos), None)

    def query_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set[MiniStaticObject|MiniDynamicObject]]:
        region = self.get_cell_region(pos, size, xdir, ydir)
        cells = set()
        for cell_pos in region:
            cell = self.cells.get(cell_pos, None)
            if cell: cells.update(cell)
        return cells

    def update_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        new_region = set(self.get_cell_region(obj.pos, obj.size))
        old_region = obj.spatial_index

        if new_region == old_region: return
        self.rem_object(obj)
        self.add_object(obj)

