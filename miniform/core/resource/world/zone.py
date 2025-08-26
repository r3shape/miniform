from miniform.imports import pg
import miniform

from .object import MiniStaticObject, MiniDynamicObject

class MiniZonePartition(miniform.MiniAtom):
    def __init__(
            self,
            
            app: "miniform.app.MiniApp",
            world: "miniform.resource.Miniworld",

            cell_size: list[int],
            zone_size: list[int],
            cell_origin: list[int] = [0, 0]
    ) -> None:
        self.cache: miniform.resource.MiniCache = app.cache
        self.world: miniform.resource.world.MiniWorld = world
        
        self.cell_origin: list[int] = [*map(int, cell_origin)]

        self.cell_width: int = int(cell_size[0])
        self.cell_height: int = int(cell_size[1])
        self.cell_size: list[int] = [*map(int, cell_size)]
        self.cell_area: int = self.cell_size[0] * self.cell_size[1]
        
        self.zone_width: int = int(cell_size[0] * zone_size[0])
        self.zone_height: int = int(cell_size[1] * zone_size[1])
        self.zone_size: list[int] = [*map(int, miniform.utils.mul_v2(zone_size, cell_size))]
        self.zone_area: int = self.zone_size[0] * self.zone_size[1]

        self.loaded_cells: set[tuple[int]] = set()
        self.loaded_zones: set[tuple[int]] = set()
        self.zones: dict[tuple[int], dict[tuple[int], set[MiniStaticObject]]] = {}

    def get_zone_pos(self, pos: list[int | float]) -> tuple[int]:
        return tuple(miniform.utils.div2_v2i(miniform.utils.sub_v2(pos, self.cell_origin), self.zone_size))

    def get_zone_region(self, pos: list[int | float], size: list[int | float], xdir: int = 0, ydir: int = 0) -> list[tuple[int]]:
        top_left = pos
        bottom_right = miniform.utils.sub_v2(miniform.utils.add_v2(pos, size), [1, 1])

        region = []
        grid_pos0 = miniform.utils.div2_v2i(top_left, self.zone_size)
        grid_pos1 = miniform.utils.div2_v2i(bottom_right, self.zone_size)
        for y in range(grid_pos0[1] - ydir, grid_pos1[1] + ydir + 1):
            for x in range(grid_pos0[0] - xdir, grid_pos1[0] + xdir + 1):
                region.append((x, y))
        return tuple(region)


    def get_cell_pos(self, pos: list[int | float]) -> tuple[int]:
        return tuple(miniform.utils.div2_v2i(miniform.utils.sub_v2(pos, self.cell_origin), self.cell_size))
    
    def get_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 0, ydir: int = 0) -> list[tuple[int]]:
        top_left = pos
        bottom_right = miniform.utils.sub_v2(miniform.utils.add_v2(pos, size), [1, 1])

        region = []
        grid_pos0 = miniform.utils.div2_v2i(miniform.utils.sub_v2(top_left, self.cell_origin), self.cell_size)
        grid_pos1 = miniform.utils.div2_v2i(miniform.utils.sub_v2(bottom_right, self.cell_origin), self.cell_size)
        for y in range(grid_pos0[1] - ydir, grid_pos1[1] + ydir + 1):
            for x in range(grid_pos0[0] - xdir, grid_pos1[0] + xdir + 1):
                region.append((x, y))
        return tuple(region)


    def load_zone(self, pos: tuple[int]) -> None:
        if pos in self.loaded_zones: return
        self.zones[pos] = {}
        self.loaded_zones.add(pos)

    def unload_zone(self, pos: tuple[int]) -> None:
        if pos not in self.loaded_zones: return
        del self.zones[pos]
        self.loaded_zones.remove(pos)


    def load_cell(self, pos: list[int]) -> None:
        zone_pos = self.get_zone_pos(miniform.utils.mul_v2(pos, self.cell_size))

        if zone_pos not in self.loaded_zones:
            self.load_zone(zone_pos)

        zone = self.zones.get(zone_pos, None)
        if zone is None: return
        
        if pos not in zone:
            zone[pos] = set()
            self.loaded_cells.add(pos)

    def unload_cell(self, pos: list[int]) -> None:
        zone_pos = self.get_zone_pos(miniform.utils.mul_v2(pos, self.cell_size))

        zone = self.zones.get(zone_pos)
        if zone and pos in zone:
            del zone[pos]
            self.loaded_cells.remove(pos)
            if len(zone) == 0:
                self.unload_zone(zone_pos)


    def add_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        obj.spatial_index.clear()
        region = self.get_cell_region(obj.pos, obj.size)
        for cell_pos in region:
            zone_pos = self.get_zone_pos(miniform.utils.mul_v2(cell_pos, self.cell_size))

            if zone_pos not in self.loaded_zones:
                self.load_zone(zone_pos)

            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            if cell_pos not in zone: self.load_cell(cell_pos)

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            if obj not in cell:
                cell.add(obj)
                obj.spatial_index.add(cell_pos)

    def rem_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        for cell_pos in obj.spatial_index:
            zone_pos = self.get_zone_pos(miniform.utils.mul_v2(cell_pos, self.cell_size))

            if zone_pos not in self.loaded_zones:
                self.load_zone(zone_pos)
                self.load_cell(cell_pos)

            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            if obj in cell:
                cell.remove(obj)

            if len(cell) == 0: self.unload_cell(cell_pos)
            if len(zone) == 0: self.unload_zone(zone_pos)
        obj.spatial_index.clear()


    def query_zone(self, pos: list[int | float]) -> set[MiniStaticObject|MiniDynamicObject]:
        zone = self.zones.get(self.get_zone_pos(pos), {})

        query = set()
        for cell in zone.values():
            query.update(cell)
        return query
    
    def query_zone_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set[MiniStaticObject|MiniDynamicObject]]:
        region = self.get_zone_region(pos, size, xdir, ydir)
        query = set()

        for zone_pos in region:
            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            for cell in zone.values():
                query.update(cell)
        return query


    def query_cell(self, pos: list[int | float]) -> set[MiniStaticObject|MiniDynamicObject]:
        zone = self.zones.get(self.get_zone_pos(pos), None)
        if zone is None: return None
        return zone.get(self.get_cell_pos(pos), set())
    
    def query_cell_region(self, pos: list[int | float], size: list[int | float], xdir: int = 2, ydir: int = 2) -> tuple[set[MiniStaticObject|MiniDynamicObject]]:
        region = self.get_cell_region(pos, size, xdir, ydir)
        query = set()

        for cell_pos in region:
            zone_pos = self.get_zone_pos(miniform.utils.mul_v2(cell_pos, self.cell_size))
            zone = self.zones.get(zone_pos, None)
            if zone is None: continue

            cell = zone.get(cell_pos, None)
            if cell is None: continue

            query.update(cell)
        return query


    def update_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        new_region = set(self.get_cell_region(obj.pos, obj.size))
        old_region = obj.spatial_index

        if new_region == old_region: return
        self.rem_object(obj)
        self.add_object(obj)
