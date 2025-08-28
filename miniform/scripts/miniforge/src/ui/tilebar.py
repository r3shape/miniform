from ..globals import miniform, pg

class MiniTile(miniform.resource.interface.MiniLabel):
    def __init__(self, key, id, world, icon, size, font) -> None:
        self.id: int = id
        self.world = world
        self.key: str = key
        super().__init__(
            icon=icon,
            size=size,
            font=font
        )

        self.color = world.theme["base-color"]
        self.text_color = world.theme["text-color"]
        self.border_color = world.theme["border-color"]

    def on_click(self):
        self.world.tile_id = self.id
        self.border_color = self.world.theme["select-color"]
    
    def on_hover(self):
        if self.world.tile_id == self.id:
            self.border_color = self.world.theme["select-color"]
        else:
            self.border_color= self.world.theme["deselect-color"]
    
    def on_unhover(self):
        self.border_color = self.world.theme["border-color"]

class MiniTileBar(miniform.resource.interface.MiniScrollContainer):
    def __init__(self, world) -> None:
        self.world = world
        super().__init__(
            speed=world.tile_map.tile_size[0]//8,
            size=[96, 256],
            wrap_x=96/world.tile_map.tile_size[0],
            wrap_y=256/world.tile_map.tile_size[1],
            pos=[0, world.app.window.size[1]/2.8],
        )

        self.color = world.theme["base-color"]
        self.border_color = world.theme["border-color"]

        self.load_tiles()

    def load_tiles(self, tileset_id: int=0) -> None:
        if tileset_id < 0 or tileset_id >= len(self.world.tile_map.tile_sets): return
        self.tileset_id = tileset_id
        self.tiles = self.world.tile_map.tile_sets[self.tileset_id][1]
        self.tile_count = len(self.world.tile_map.tile_sets[self.tileset_id][1])
        self.tile_size = [*map(lambda t: t* 2 if t < 16 else t, self.world.tile_map.tile_size)]
        self.tiles = [pg.transform.scale(tile, self.tile_size) for tile in self.world.tile_map.tile_sets[self.tileset_id][1]]

        for i, t in enumerate(self.tiles):
            key = f"tile{i}"
            self.set_element(key, MiniTile(
                id=i,
                key=key,
                world=self.world,
                icon=self.tiles[i],
                size=self.tile_size,
                font=self.world.cache.get_font("slkscr")
            ))
