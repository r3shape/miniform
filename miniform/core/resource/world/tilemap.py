from miniform.imports import pg, os, json, random
import miniform

from .object import MiniStaticObject, MiniDynamicObject

class MiniTileMap(miniform.MiniAtom):
    def __init__(
            self,
            world: "miniform.resource.world.MiniWorld",
            
            tile_size: list[int],
            tile_origin: list[int]=[0, 0],
            tile_color: list[int]=[0, 0, 255]) -> None:
            # tile_color: list[int]=[172, 50, 50]) -> None:
        super().__init__()
        self.world: miniform.resource.world.MiniWorld = world
        self.configure(tile_size, tile_origin, tile_color)

    def configure(
            self,
            tile_size: list[int],
            tile_origin: list[int]=[0, 0],
            tile_color: list[int]=[172, 50, 50]) -> None:
                
        self.tile_count: int = 0
        # self.tile_data[l: int][(x: int,y: int)] = [tid, static, sid, object]
        self.tile_data: dict[str, list] = {0: {}}
        self.tile_vertices: list[list[int]] = None
        # self.tile_sets[ts: int] = [tsp: str, surfs: list[pg.Surface]]
        self.tile_sets: list[list[str, pg.Surface]] = []
        self.tile_size: list[int] = [*map(int, tile_size)]
        self.tile_color: list[int] = [*map(int, tile_color)]
        self.tile_origin: list[int] = [*map(int, tile_origin)]

    @property
    def size(self) -> list[int]:
        if not any(self.tile_data.values()):
            return [0, 0]

        gx_min = gy_min = float("inf")
        gx_max = gy_max = float("-inf")

        for layer in self.tile_data.values():
            for gx, gy in layer.keys():
                gx_min = min(gx_min, gx)
                gy_min = min(gy_min, gy)
                gx_max = max(gx_max, gx)
                gy_max = max(gy_max, gy)

        wx_min, wy_min = miniform.utils.mul_v2([gx_min, gy_min], self.tile_size)
        wx_max, wy_max = miniform.utils.mul_v2([gx_max + 1, gy_max + 1], self.tile_size)  # +1 to include full tile

        return [wx_max - wx_min, wy_max - wy_min]

    def _gen_region(self, size:list[int], pos:list[int]) -> list[list[int]]:
        region = []
        cx, cy = map(int, miniform.utils.div2_v2i(pos, self.tile_size))
        for x in range(cx - size[0], (cx + size[0]) + 1):
            for y in range(cy - size[1], (cy + size[1]) + 1):
                region.append([x, y])
        return region
    
    def _gen_vertices(self, layer: int) -> None:
        data = self.tile_data.get(layer, None)
        if data is None or len(data) == 0: return
        tiles = self.all_tiles(layer)
        
        X = 0; Y = 1
        START = 0; END = 1
        TX , TY = self.tile_size
        NORTH = 0; SOUTH = 1; EAST = 2; WEST = 3

        # scanline-sort
        tiles.sort(key=lambda t: t.pos[0])
        tiles.sort(key=lambda t: t.pos[1])

        poly_map = {}
        poly_ids = {}
        for i, tile in enumerate(tiles):
            gx, gy = miniform.utils.div2_v2i(tile.pos, self.tile_size)
            poly_ids[(gx, gy)] = i
            poly = {}

            # no north tile
            if (ntile := (data.get((gx, gy - 1), False))) == False:
                if (wtile := (data.get((gx - 1, gy), False))) != False\
                and wtile[-1].get_flag(miniform.MiniObjectFlag.OBJECT_N_EDGE):
                    ngx, ngy = miniform.utils.div2_v2i(wtile[-1].pos, self.tile_size)
                    poly_map[poly_ids[(ngx, ngy)]][NORTH][END][X] += TX
                    poly[NORTH] = poly_map[poly_ids[(ngx, ngy)]][NORTH]
                else: poly[NORTH] = [tile.top_left, tile.top_right]
                tile.set_flag(miniform.MiniObjectFlag.OBJECT_N_EDGE)
            else: tile.rem_flag(miniform.MiniObjectFlag.OBJECT_N_EDGE)

            # no south tile
            if (stile := (data.get((gx, gy + 1), False))) == False:
                if (wtile := (data.get((gx - 1, gy), False))) != False\
                and wtile[-1].get_flag(miniform.MiniObjectFlag.OBJECT_S_EDGE):
                    ngx, ngy = miniform.utils.div2_v2i(wtile[-1].pos, self.tile_size)
                    poly_map[poly_ids[(ngx, ngy)]][SOUTH][END][X] += TX
                    poly[SOUTH] = poly_map[poly_ids[(ngx, ngy)]][SOUTH]
                else: poly[SOUTH] = [tile.bottom_left, tile.bottom_right]
                tile.set_flag(miniform.MiniObjectFlag.OBJECT_S_EDGE)
            else: tile.rem_flag(miniform.MiniObjectFlag.OBJECT_S_EDGE)

            # no east tile
            if (etile := (data.get((gx + 1, gy), False))) == False:
                if (ntile := (data.get((gx, gy - 1), False))) != False\
                and ntile[-1].get_flag(miniform.MiniObjectFlag.OBJECT_E_EDGE):
                    ngx, ngy = miniform.utils.div2_v2i(ntile[-1].pos, self.tile_size)
                    poly_map[poly_ids[(ngx, ngy)]][EAST][END][Y] += TY
                    poly[EAST] = poly_map[poly_ids[(ngx, ngy)]][EAST]
                else: poly[EAST] = [tile.top_right, tile.bottom_right]
                tile.set_flag(miniform.MiniObjectFlag.OBJECT_E_EDGE)
            else: tile.rem_flag(miniform.MiniObjectFlag.OBJECT_E_EDGE)

            # no west tile
            if (wtile := (data.get((gx - 1, gy), False))) == False:
                if (ntile := (data.get((gx, gy - 1), False))) != False\
                and ntile[-1].get_flag(miniform.MiniObjectFlag.OBJECT_W_EDGE):
                    ngx, ngy = miniform.utils.div2_v2i(ntile[-1].pos, self.tile_size)
                    poly_map[poly_ids[(ngx, ngy)]][WEST][END][Y] += TY
                    poly[WEST] = poly_map[poly_ids[(ngx, ngy)]][WEST]
                else: poly[WEST] = [tile.top_left, tile.bottom_left]
                tile.set_flag(miniform.MiniObjectFlag.OBJECT_W_EDGE)
            else: tile.rem_flag(miniform.MiniObjectFlag.OBJECT_W_EDGE)
            poly_map[i] = poly
        self.tile_vertices = [v for id, poly in poly_map.items() for v in poly.values()]

    def import_tile_set(self, path: str) -> bool:
        path = path
        if not os.path.exists(path):
            miniform.MiniLogger.error(f"[MiniTileMap] failed to import tile_set: (path){path}")
            return False
        self.tile_sets.append([path, miniform.utils.load_surface_array(path, self.tile_size)])
        miniform.MiniLogger.info(f"[MiniTileMap] imported tile_set: (path){path}")
        return True
    
    def import_data(self, name: str, path: str) -> bool:
        self.clear()

        path = path
        if not os.path.exists(path):
            miniform.MiniLogger.error(f"[MiniTileMap] failed to import tilemap data: (path){path}")
            return False
        
        path = os.path.join(path, f"{name}.json")
        with open(path, "r") as save:
            data = json.load(save)
            
            config: dict = data["config"]
            tile_data: dict = data["tile_data"]

            self.configure(config["tile_size"], config["tile_origin"], config["tile_color"])
            
            tile_sets = config["tile_sets"]
            for i, tile_set in enumerate(tile_sets):
                if os.path.exists(tile_set):
                    self.tile_sets.append([tile_set, miniform.utils.load_surface_array(tile_set, self.tile_size)])
                else:
                    miniform.MiniLogger.error(f"[MiniTileMap] tile_set not found: {tile_set}")
                    return False
            
            for layer in tile_data:
                for pos, data, in tile_data[layer].items():
                    pos = miniform.utils.mul_v2([*map(float, pos.split(","))], self.tile_size)
                    self.set_tile(layer, pos, *data)
        
        miniform.MiniLogger.info(f"[MiniTileMap] imported tilemap data: (path){path}")
        return True
    
    def export_data(self, name: str, path: str) -> bool:
        path = path
        if not os.path.exists(path):
            miniform.MiniLogger.error(f"[MiniTileMap] failed to export tilemap data: (name){name} (path){path}")
            return False

        tile_sets = []
        for tile_set_path, tiles in self.tile_sets:
            tile_sets.append(tile_set_path)
        
        save_data = {
            "config": {
                "tile_size": self.tile_size,
                "tile_origin": self.tile_origin,
                "tile_color": self.tile_color,
                "tile_sets": tile_sets
            },
            "tile_data": {}
        }

        for layer in self.tile_data:
            save_data["tile_data"][layer] = {}
            for tile_pos in self.tile_data[layer]:
                tile_data = self.tile_data[layer][tile_pos]
                save_data["tile_data"][layer][f"{tile_pos[0]},{tile_pos[1]}"] = tile_data[:-1]

        with open(os.path.join(path, f"{name}.json"), "w") as save:
            try:
                json.dump(save_data, save, indent=4, separators=(",", ": "), )
            except json.JSONDecodeError as e: return False
        
        miniform.MiniLogger.info(f"[MiniTileMap] exported tilemap data: (name){name} (path){path}")
        return True

    def clear(self) -> None:
        for layer in self.tile_data:
            for tile_pos in self.tile_data[layer]:
                _, __, ___, tile_object = self.tile_data[layer][tile_pos]
                self.world.rem_object(tile_object)
        
        self.tile_data = {0: {}}

    """ TILE OBJECT """
    def all_tiles(self, layer: int) -> list[MiniStaticObject|MiniDynamicObject]:
        return [tile[3] for tile in self.tile_data[layer].values()]

    def set_tile(self, layer: int, pos: list[int], tile: int, tile_set: int, static: bool=True, regen: bool=True) -> None:
        layer = int(layer)
        if self.tile_data.get(layer, False) == False:
            miniform.MiniLogger.warning(f"[MiniTileMap] tilemap layer not found: (layer){layer}, {self.tile_data}")
            return

        gx, gy = miniform.utils.div2_v2i(pos, self.tile_size)
        if self.tile_data[layer].get((gx, gy), False) != False:
            miniform.MiniLogger.warning(f"[MiniTileMap] tile present: (layer){layer} (pos){[gx, gy]}")
            return

        tile_object = self.world.load_object(f"{[gx, gy]}", self.tile_size, miniform.utils.mul_v2([gx, gy], self.tile_size), color=self.tile_color, static=static)

        if tile < 0 or tile_set < 0 or tile_set >= len(self.tile_sets):
            miniform.MiniLogger.warning(f"[MiniTileMap] tile/tile_set index out of range: (tile){tile} (tile_set){tile_set}")
        else:
            tile_object.surface = self.tile_sets[tile_set][1][tile]
        
        self.tile_count += 1
        self.tile_data[layer][(gx, gy)] = [tile, tile_set, static, tile_object]
        
        if regen: self._gen_vertices(layer)
        
        miniform.MiniLogger.info(f"[MiniTileMap] set tile: (layer){layer} (tile){tile} (tile_set){tile_set} (pos){gx, gy} (static){static}")

    def get_tile(self, layer: int, pos: list[int]) -> MiniStaticObject|MiniDynamicObject|None:
        gx, gy = miniform.utils.div2_v2i(pos, self.tile_size)
        if self.tile_data.get(layer, False) == False:
            miniform.MiniLogger.warning(f"[MiniTileMap] failed to get tile: (layer){layer} (pos){[gx, gy]}")
            return
        return self.tile_data[layer].get((gx, gy), None)
    
    def rem_tile(self, layer: int, pos: list[int], regen: bool=True) -> None:
        if self.tile_data.get(layer, False) == False:
            miniform.MiniLogger.warning(f"[MiniTileMap] tilemap layer not found: (layer){layer}")
            return
        
        gx, gy = miniform.utils.div2_v2i(pos, self.tile_size)
        if self.tile_data[layer].get((gx, gy), False) == False:
            miniform.MiniLogger.warning(f"[MiniTileMap] tile not present: (layer){layer} (pos){[gx, gy]}")
            return
        
        tile, tile_set, static, tile_object = self.tile_data[layer][(gx, gy)]
        self.world.rem_object(tile_object)

        self.tile_count -= 1
        del self.tile_data[layer][(gx, gy)]
        
        if regen: self._gen_vertices(layer)
        
        miniform.MiniLogger.info(f"[MiniTileMap] rem tile: (layer){layer} (tile){tile} (tile_set){tile_set} (pos){gx, gy} (static){static}")

    def get_tile_region(self, layer: int, size:list[int], pos:list[int]) -> list[MiniStaticObject|MiniDynamicObject]:
        if self.tile_data.get(layer, False) == False: return
        
        tiles = []
        region = self._gen_region(size, pos)
        for gx, gy in region:
            tile = self.tile_data[layer].get((gx, gy), None)
            if tile: tiles.append(tile)
        return tiles

    def rem_tile_region(self, layer: int, size:list[int], pos:list[int], regen: bool=True) -> None:
        if self.tile_data.get(layer, False) == False: return
        
        region = self._gen_region(size, pos)
        for gx, gy in region:
            self.rem_tile(layer, miniform.utils.mul_v2([gx, gy], self.tile_size), 0)
        
        if regen: self._gen_vertices(layer)
    
    def set_tile_region(self, layer: int, size:list[int], pos:list[int], tile: int, tile_set: int, static: bool=True, regen: bool=True) -> None:
        if self.tile_data.get(layer, False) == False: return
        
        region = self._gen_region(size, pos)
        for gx, gy in region:
            self.set_tile(layer, miniform.utils.mul_v2([gx, gy], self.tile_size), tile, tile_set, static, 0)
        
        if regen: self._gen_vertices(layer)
