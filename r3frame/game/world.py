from r3frame.globs import re, pg, random
from r3frame.game.obj import Object

# ------------------------------------------------------------ #
class Tilemap(Object):
    def __init__(self, size: list[int], tilesize: int=32, grid_color: list[int]=[10, 10, 10]) -> None:
        self._ = pg.Surface([tilesize, tilesize])
        self._.fill([255, 255, 255])

        self.sizet = size                                       # in tiles
        self.width = size[0]                                    # in tiles
        self.height = size[1]                                   # in tiles
        self.tilesize = tilesize                                # in pixels
        self.data = [None for _ in range(self.sizet[0] * self.sizet[1])]
        self.tiles = [None for _ in range(self.sizet[0] * self.sizet[1])]
        self.sizep: list[int] = [self.sizet[0] * self.tilesize, self.sizet[1] * self.tilesize]

        self.grid_color: list[int] = grid_color

        super().__init__(self.sizep, [255, 255, 255], [0, 0], 1000)

    def export_data(self, path: str) -> bool:
        with open(path, "w") as save:
            for c in map(str, self.data):
                save.write(c)
        return True
    
    def import_data(self, path:str) -> bool:
        with open(path, "r") as save:
            data = re.split(r'(\d)', save.read())
            data = [t for t in data if t != '']
            for i in range(len(data)):
                try: data[i] = int(data[i])
                except: pass
            self.data = data
        return True
    
    def load_data(self) -> None:
        if not isinstance(self.data, list): return
        for x in range(self.sizet[0]):
            for y in range(self.sizet[1]):
                data_tile = self.data[y * self.sizet[0] + x]
                if data_tile != 0 and data_tile != None:
                    tile = Object(
                        size=[self.tilesize, self.tilesize], color=[255, 255, 255],
                        location=[x * self.tilesize, y * self.tilesize]
                    )
                    tile.id = data_tile
                    self.tiles[y * self.sizet[0] + x] = tile

    def set_data(self, location: list[int], data: int|str) -> None:
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return
        self.data[mapy * self.sizet[0] + mapx] = data
    
    def rem_data(self, location: list[int]) -> None:
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return
        self.data[mapy * self.sizet[0] + mapx] = None

    def get_data(self, location: list[int]) -> int|str|None:
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return None
        return self.data[mapy * self.sizet[0] + mapx]

    def read_data(self, data: list[int|str]) -> None:
        for x in range(self.sizet[0]):
            for y in range(self.sizet[1]):
                self.set_data([x * self.tilesize, y * self.tilesize], data[y * self.sizet[0] + x])
    
    def get_tile(self, location: list[int]) -> int:
        location = [
            int(location[0] - self.location[0]),
            int(location[1] - self.location[1])
        ]
        mapx = location[0] // self.tilesize
        mapy = location[1] // self.tilesize
        if mapx < 0 or mapy < 0 or mapx >= self.sizet[0] or mapy >= self.sizet[1]: return None
        return self.tiles[mapy * self.sizet[0] + mapx]

    def set_tile(self, tile_id: int, location: list[int]) -> None:
        if self.get_tile(location) is not None: return
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
        
        index = location[1] // self.tilesize * self.sizet[0] + location[0] // self.tilesize
        self.data[index] = tile_id
        self.tiles[index] = tile
        self.image.blit(self.tiles[index].image, [mapx, mapy])

    def rem_tile(self, location: list[int]) -> None:
        if self.get_tile(location) is None: return
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
        self.data[index] = None
        self.tiles[index] = None

    def _generate_region(self, size:list[int], location:list[int]) -> list[list[int]]:
        center = [
            int(location[0] // self.tilesize),
            int(location[1] // self.tilesize)
        ]; region = []
        for x in range(center[0] - size[0], (center[0] + size[0]) + 1):
            for y in range(center[1] - size[1], (center[1] + size[1]) + 1):
                region.append([x, y])
        return region

    def get_region(self, size:list[int], location:list[int]) -> list[Object]|None:
        region = self._generate_region(size, location)
        if not region: return None
        tiles = []
        for map_location in region:
            index = map_location[1] * self.sizet[0] + map_location[0]
            if index < 0 or index >= (self.sizet[0] * self.sizet[1]): continue
            tile = self.tiles[index]
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
