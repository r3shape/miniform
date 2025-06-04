from blakbox.atom import BOXatom
from blakbox.utils import div2_v2i, mul_v2
from blakbox.globals import os, pg, json, random
from blakbox.scene.objectgrid import BOXobjectgrid, BOXobject

# ------------------------------------------------------------ #
class BOXtilemap(BOXatom):
    def __init__(
            self, scene,
            tile_size: list[int],
            grid_size: list[int],
        ) -> None:
        self._config(scene, tile_size, grid_size)
    
    def _config(self,scene,
            tile_size: list[int],
            grid_size: list[int],) -> None:
        self.scene = scene
        self.grid: BOXobjectgrid = BOXobjectgrid(tile_size, grid_size)  # spatial partitioning (tracks dynamic/static objects using BOXobject.grid_cell field)

        self.tile_size: list[int] = tile_size
        self.grid_size: list[int] = grid_size
        self.surf_size: list[int] = [tile_size[0] * grid_size[0], tile_size[1] * grid_size[1]]

        self.tilesets: list[pg.Surface] = []

        # self.layers[layer][0] = tile data layer
        # self.layers[layer][1] = tile object layer
        self.layers: dict[str, list] = {
            "bg": [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)],
            "fg": [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)],
            "mg":  [[None for _ in range(grid_size[0] * grid_size[1])] for _ in range(2)]
        }

    def _gen_region(self, size:list[int], pos:list[int]) -> list[list[int]]:
        region = []
        cx, cy = map(int, div2_v2i(pos, self.tile_size))
        for x in range(cx - size[0], (cx + size[0]) + 1):
            for y in range(cy - size[1], (cy + size[1]) + 1):
                region.append([x, y])
        return region

    """ TILE OBJECT """
    def all_tiles(self, layer:str) -> list[BOXobject]:
        return self.layers[layer][1]

    def set_tile(self, layer: str, pos: list[int], tile: int, tileset: int) -> None:
        if tile < 0 or tileset < 0: return
        if not self.layers.get(layer, False): return
        
        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return
        
        if self.layers[layer][1][index] is not None: return

        tile_object = BOXobject(
            size=self.tile_size,
            pos=mul_v2(div2_v2i(pos, self.tile_size), self.tile_size),
            color=[random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        ); tile_object.id = tile; tile_object.surface = self.tilesets[tileset][1][tile]

        self.scene.resource.store_object(f"tile-{tile_object.pos}", tile_object)
        self.grid.set(tile_object)

        self.layers[layer][0][index] = [tile, tileset]
        self.layers[layer][1][index] = tile_object

    def get_tile(self, layer: str, pos: list[int]) -> BOXobject:
        if not self.layers.get(layer, False): return
        
        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        # return self.scene.resource.get_object(f"tile-{self.layers[layer][1][index].pos}")
        return self.layers[layer][1][index]
    
    def rem_tile(self, layer: str, pos: list[int]) -> None:
        if not self.layers.get(layer, False): return
        
        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        if self.layers[layer][1][index] == None: return
        
        self.scene.resource.rem_object(f"tile-{self.layers[layer][1][index].pos}")
        self.grid.rem(self.layers[layer][1][index])
        
        self.layers[layer][0][index] = None
        self.layers[layer][1][index] = None

    def get_tile_region(self, layer:str, size:list[int], pos:list[int]) -> list[BOXobject]:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        tiles = []
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): continue
            tile = self.layers[layer][1][index]
            if tile: tiles.append(tile)
        return tiles

    def rem_tile_region(self, layer:str, size:list[int], pos:list[int]) -> None:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): continue
            if self.layers[layer][1][index] == None: continue
            
            self.scene.resource.rem_object(f"tile-{self.layers[layer][1][index].pos}")
            self.layers[layer][1][index] = None

        self.grid.rem_region(size, pos)

    """ TILE DATA """
    def import_data(self, path:str) -> bool:
        if not os.path.exists(path): return False
        with open(path, "r") as save:
            data = json.load(save)
            
            config: dict = data["config"]
            layers: dict = data["layers"]

            self._config(self.scene, config["tile_size"], config["grid_size"])
            
            tilesets = config["tilesets"]
            for i, tileset in enumerate(tilesets):
                if os.path.exists:
                    self.tilesets.append([tileset, self.scene.resource.pg_load_surface_sheet(tileset, self.tile_size)])
                else:
                    print(f"Path Not Found: {tileset}")
                    return False
            
            for layer in layers:
                for pos, data, in layers[layer].items():
                    if data[0] in (-1, None): continue
                    pos = mul_v2([*map(int, pos.split(","))], self.tile_size)
                    self.set_tile(layer, pos, data[0], data[1])
        return True
    
    def export_data(self, path: str) -> bool:
        if not os.path.exists(path): return False

        tilesets = []
        for tileset_path, tiles in self.tilesets:
            tilesets.append(tileset_path)
        
        save_data = {
            "config": {
                "tile_size": self.tile_size,
                "grid_size": self.grid_size,
                "tilesets": tilesets
            },
            "layers": {}
        }

        for layer in self.layers:
            save_data["layers"][layer] = {}
            for tile in self.layers[layer][1]:
                if tile is None: continue
                gx, gy = div2_v2i(tile.pos, self.tile_size)
                index = int(gy * self.tile_size[0] + gx)
                save_data["layers"][layer][f"{gx},{gy}"] = self.layers[layer][0][index]
                
        with open(path, "w") as save:
            try:
                json.dump(save_data, save, indent=4, separators=(",", ": "), )
            except json.JSONDecodeError as e: return False
        return True
    
    def all_data(self, layer:str) -> list[BOXobject]:
        return self.layers[layer][0]

    def set_data(self, layer: str, pos: list[int], tile: int, tileset: int) -> None:
        if tile < 0 or tileset < 0: return
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        self.layers[layer][0][index] = [tile, tileset]

    def get_data(self, layer: str, pos: list[int]) -> list[int]:
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        return self.layers[layer][0][index]

    def rem_data(self, layer: str, pos: list[int]) -> None:
        if not self.layers.get(layer, False): return

        gx, gy = div2_v2i(pos, self.tile_size)
        if gx < 0 or gy < 0 or gx >= self.grid_size[0] or gy >= self.grid_size[1]: return

        index = int(gy * self.tile_size[0] + gx)
        if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): return

        self.layers[layer][0][index] = None

    def set_data_region(self, layer:str, size:list[int], pos:list[int], tile: int, tileset: int) -> None:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): continue
            self.layers[layer][0][index] = [tile, tileset]
    
    def get_data_region(self, layer:str, size:list[int], pos:list[int]) -> list[BOXobject]:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        datas = []
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): continue
            data = self.layers[layer][0][index]
            if data: datas.append(data)
        return datas

    def rem_data_region(self, layer:str, size:list[int], pos:list[int]) -> None:
        if not self.layers.get(layer, False): return
        
        region = self._gen_region(size, pos)
        if not region: return None
        
        for gx, gy in region:
            index = int(gy * self.tile_size[0] + gx)
            if index < 0 or index >= (self.tile_size[0] * self.tile_size[1]): continue
            self.layers[layer][0][index] = None
# ------------------------------------------------------------ #