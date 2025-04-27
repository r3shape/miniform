from r3frame.globs import os, re, pg, json, random
from r3frame.app.resource.image import Image
from r3frame.util import unequal_arrays
from r3frame.game.obj import Object

# ------------------------------------------------------------ #
class Tilemap(Object):
    def __init__(self, app, size: list[int], tilesize: int=32, grid_color: list[int]=[10, 10, 10]) -> None:
        self._ = pg.Surface([tilesize, tilesize])
        self._.fill([255, 255, 255])
        self.app = app
        self.sizet = size                                                                       # in tiles
        self.width = size[0]                                                                    # in tiles
        self.height = size[1]                                                                   # in tiles
        self.tilesize = tilesize                                                                # in pixels
        self.sizep: list[int] = [self.sizet[0] * self.tilesize, self.sizet[1] * self.tilesize]  # in pixels

        self.tilesets: list[Image] = []
        self.layers: dict[str, list] = {
            "background": [[None for _ in range(self.sizet[0] * self.sizet[1])] for _ in range(2)],
            "foreground": [[None for _ in range(self.sizet[0] * self.sizet[1])] for _ in range(2)],
            "midground": [[None for _ in range(self.sizet[0] * self.sizet[1])] for _ in range(2)]
        }

        self.grid_color: list[int] = grid_color

        super().__init__([0, 0], self.sizep, [255, 255, 255])

    def export_image(self, name: str, path: str, grid: bool=False) -> None:
        if not os.path.exists(path): return False
        for i in range(len(self.tilesets)):
            for layer in self.layers:
                self.read_data(layer, i, self.sizet, self.tilesize, self.layers[layer][0])
        if grid: self.render_grid()
        pg.image.save(self.image, os.path.join(path, f"{name}.png"))

    def read_data(self, layer: str, tileset: int, sizet: list[int], tilesize:int, data: list[int|str]) -> None:
        if tileset < 0 or tileset >= len(self.tilesets): return
        if not self.layers.get(layer, False): return
        for x in range(sizet[0]):
            for y in range(sizet[1]):
                data_tile = data[y * sizet[0] + x]
                if data_tile != -1 and data_tile != None:
                    self.set_tile(layer, tileset, data_tile, [x * tilesize, y * tilesize])

    def export_data(self, path: str) -> bool:
        if not os.path.exists(path): return False

        tilesets = []
        for ts in self.tilesets:
            for tileset in ts:
                if len(tilesets) and tileset.path == tilesets[len(tilesets)-1]:
                    continue
                tilesets.append(tileset.path)
        
        save_data = {
            "config": {
                "tilesize": self.tilesize,
                "sizet": self.sizet,
                "tilesets": tilesets
            },
            "layers": {}
        }

        for layer in self.layers:
            save_data["layers"][layer] = {}
            for tile in self.layers[layer][1]:
                if tile is None: continue
                location = [
                    tile.location[0] // self.tilesize,
                    tile.location[1] // self.tilesize
                ]
                index = location[1] * self.sizet[0] + location[0]
                location = f"{location[0]},{location[1]}"
                save_data["layers"][layer][location] = self.layers[layer][0][index]
                
        with open(path, "w") as save:
            try:
                json.dump(save_data, save, indent=4, separators=(",", ": "))
            except json.JSONDecodeError as e: return False
        return True
    
    def import_data(self, path:str) -> bool:
        if not os.path.exists(path): return False
        with open(path, "r") as save:
            data = json.load(save)
            
            config: dict = data["config"]
            layers: dict = data["layers"]

            sizet = config["sizet"]
            tilesize = config["tilesize"]
            
            tilesets = config["tilesets"]
            for i, tileset in enumerate(tilesets):
                if not os.path.exists:
                    print(f"failed to load tileset: {tileset}")
                    return False
                self.tilesets.append(self.app.resource.load_image_sheet(
                    f"tileset{i}", tileset, [tilesize, tilesize]
                ))

            for layer in layers:
                for location, data in layers[layer].items():
                    location = [*map(int, location.split(","))]
                    if data[0] != -1 and data[0] != None:
                        self.set_tile(layer, data[0], data[1], [location[0] * tilesize, location[1] * tilesize])
        return True
    
    def import_tileset(self, path: str) -> bool:
        if not os.path.exists(path): return False
        self.tilesets.append(self.app.resource.load_image_sheet(f"tileset{len(self.tilesets)-1}", path, [self.tilesize, self.tilesize]))
        return True

    def set_data(self, layer: str, tileset: int, tile_id: int, location: list[int]) -> None:
        if tileset < 0 or tileset >= len(self.tilesets): return
        if not self.layers.get(layer, False): return
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return
        self.layers[layer][0][mapy * self.sizet[0] + mapx] = [tileset, tile_id]
    
    def rem_data(self, layer: str, location: list[int]) -> None:
        if not self.layers.get(layer, False): return
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return
        self.layers[layer][0][mapy * self.sizet[0] + mapx] = None

    def get_data(self, layer: str, location: list[int]) -> int|str|None:
        if not self.layers.get(layer, False): return
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return None
        return self.layers[layer][0][mapy * self.sizet[0] + mapx]
    
    def get_tile(self, layer: str, location: list[int]) -> int:
        if not self.layers.get(layer, False): return
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return None
        return self.layers[layer][1][mapy * self.sizet[0] + mapx]

    def set_tile(self, layer: str, tileset: int, tile_id: int, location: list[int]) -> None:
        if tileset < 0 or tileset >= len(self.tilesets): return
        if not self.layers.get(layer, False): return
        if self.get_tile(layer, location) is not None: return
        
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]

        mapx = (location[0] * self.tilesize) // self.tilesize
        mapy = (location[1] * self.tilesize) // self.tilesize
        mapx -= mapx % self.tilesize
        mapy -= mapy % self.tilesize
        if (
            mapx < 0 or mapx > self.size[0] or mapx + self.tilesize > self.size[0] or
            mapy < 0 or mapy > self.size[1] or mapy + self.tilesize > self.size[1]
            ): return
        
        tile = Object(
            size=[self.tilesize, self.tilesize], color=[
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ], location=[
                (location[0] // self.tilesize) * self.tilesize,
                (location[1] // self.tilesize) * self.tilesize
            ]
        )

        tile.id = tile_id

        if tile_id < 0 or tile_id >= len(self.tilesets[tileset]): pass
        else:
            tile.image = self.tilesets[tileset][tile_id]
            self.image.blit(tile.image.data, [mapx, mapy])
        
        index = location[1] // self.tilesize * self.sizet[0] + location[0] // self.tilesize
        self.layers[layer][0][index] = [tileset, tile_id]
        self.layers[layer][1][index] = tile

    def rem_tile(self, layer: str, location: list[int]) -> None:
        if not self.layers.get(layer, False): return
        if self.get_tile(layer, location) is None: return
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]

        mapx = (location[0] * self.tilesize) // self.tilesize
        mapy = (location[1] * self.tilesize) // self.tilesize
        mapx -= mapx % self.tilesize
        mapy -= mapy % self.tilesize
        if (
            mapx < 0 or mapx > self.size[0] or mapx + self.tilesize > self.size[0] or
            mapy < 0 or mapy > self.size[1] or mapy + self.tilesize > self.size[1]
            ): return
        
        self.image.blit(self._, [mapx, mapy])
        index = location[1] // self.tilesize * self.sizet[0] + location[0] // self.tilesize
        self.layers[layer][0][index] = None
        self.layers[layer][1][index] = None

    def _generate_region(self, size:list[int], location:list[int]) -> list[list[int]]:
        center = [
            int(location[0] // self.tilesize),
            int(location[1] // self.tilesize)
        ]; region = []
        for x in range(center[0] - size[0], (center[0] + size[0]) + 1):
            for y in range(center[1] - size[1], (center[1] + size[1]) + 1):
                region.append([x, y])
        return region

    def get_region(self, layer:str, size:list[int], location:list[int]) -> list[Object]|None:
        if not self.layers.get(layer, False): return
        region = self._generate_region(size, location)
        if not region: return None
        tiles = []
        for map_location in region:
            index = map_location[1] * self.sizet[0] + map_location[0]
            if index < 0 or index >= (self.sizet[0] * self.sizet[1]): continue
            tile = self.layers[layer][1][index]
            if tile: tiles.append(tile)
        return tiles

    def render_grid(self) -> None:
        start = [0, 0]
        end = [
            (start[0] + (self.sizet[0] * self.tilesize)) // self.tilesize,
            (start[1] + (self.sizet[1] * self.tilesize)) // self.tilesize
        ]
        
        for gx in range(int(start[0]), int(end[0])):
            x = gx * self.tilesize
            pg.draw.line(self.image, self.grid_color, [x, start[1] * self.tilesize], [x, end[1] * self.tilesize], 1)
        
        for gy in range(int(start[1]), int(end[1])):
            y = gy * self.tilesize
            pg.draw.line(self.image, self.grid_color, [start[0] * self.tilesize, y], [end[0] * self.tilesize, y], 1)
# ------------------------------------------------------------ #
