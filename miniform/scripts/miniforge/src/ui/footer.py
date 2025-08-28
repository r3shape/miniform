from ..globals import miniform, pytz, datetime

class MiniFooter(miniform.resource.interface.MiniLabel):
    def __init__(self, world) -> None:
        self.world = world
        super().__init__(
            world.cache.get_font("slkscr"),
            text="MiniForge",
            text_pos=[8, 8],
            size=[world.app.window.size[0], 100],
            flags=miniform.MiniElementFlag.SHOW_TEXT
        )
        self.sections: int = 5

        self.color = world.theme["base-color"]
        self.text_color = world.theme["text-color"]
        self.border_color = world.theme["border-color"]
        self.pos = [0, world.app.window.size[1]-100]

        self.set_flag(miniform.MiniElementFlag.SHOW_BORDER)
    
    def on_render(self, surface):
        self.set_text(f"{datetime.today().astimezone(pytz.timezone("US/Eastern")).strftime("%I:%M %p")}", [8, 32])

        if self.world.map_loaded:
            self.set_text(f"{self.world.tile_map.tile_size[0]}x{self.world.tile_map.tile_size[1]}", [8, 52])
            self.set_text(f"{self.world.tile_map.size[0]}x{self.world.tile_map.size[1]}", [8, 72])
            
            tiles = len(self.world.tile_map.tile_data[self.world.tile_layer])
            tw, th = self.world.tile_map.tile_size
            mw, mh = self.world.tile_map.size
            mw, mh = [mw // tw, mh // th]
            total = mw * mh
            
            epsilon = 0.00000001
            percent = (tiles + epsilon) / (total + epsilon)

            colors = [[255,0,0], [255,255,0], [0,255,0], [100,100,255]]
            bars = int(percent * len(colors))

            bw, bh = [8, 8]
            bx, by = [self.size[0] - (bw * len(colors) + 8), 10]

            for i in range(len(colors)):
                miniform.utils.draw_rect(surface, [bw, bh], [bx + i*bw, by], colors[i] + [255 * ((percent * 200) / 200)], 0 if i < bars else 1)
                miniform.utils.draw_rect(surface, [bw, bh], [bx + i*bw, by], colors[i], 1)
