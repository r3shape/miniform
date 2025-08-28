from ..globals import miniform

class MiniToolButton(miniform.resource.interface.MiniElement):
    def __init__(self, world, _type: str, pos: list[int]) -> None:
        self.world = world
        super().__init__(
            pos=pos[:],
            size=[18*3.5, 16],
            color=world.theme["base-color"],
            border_color=world.theme["border-color"]
        )

        self._type = _type
        self.icon_pos = [18, 0]

        if self._type.lower() == "draw":
            self.tile_id = 2
        if self._type.lower() == "eraser":
            self.tile_id = 0
        if self._type.lower() == "fill":
            self.tile_id = 3

    def on_hover(self) -> None:
        if self.world.tile_id == self.tile_id:
            self.border_color = self.world.theme["select-color"]
        else:
            self.border_color= self.world.theme["deselect-color"]

    def on_unhover(self) -> None:
        self.border_color = self.world.theme["border-color"]

    def on_click(self) -> None:
        self.world.tile_id = self.tile_id
        self.border_color = self.world.theme["select-color"]

    def on_render(self, surface):
        surface.blit(self.world.cache.get_surface(self._type), self.icon_pos)
        
class MiniToolBar(miniform.resource.interface.MiniLabel):
    def __init__(self, world) -> None:
        self.world = world
        super().__init__(
            world.cache.get_font("slkscr"),
            text="tools",
            size=[96, 256],
            text_pos=[14, 0],
            flags=miniform.MiniElementFlag.SHOW_TEXT
        )
        
        self.pos=[world.app.window.size[0]-96, world.app.window.size[1]/2.8]
        self.color= self.world.theme["base-color"]

        self.border_size = [2, 2]
        self.border_color = self.world.theme["border-color"]

        self.set_element("red-btn", MiniToolButton(world, "draw", [16, 32]))
        self.set_element("green-btn", MiniToolButton(world, "eraser", [16, 64]))
        self.set_element("blue-btn", MiniToolButton(world, "fill", [16, 96]))
