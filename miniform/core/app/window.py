from miniform.imports import pg
import miniform

class MiniWindow(miniform.MiniAtom):
    def __init__(self, title: str="R3N Window", size: list[int]=[1280, 720], color: list[int]=[55, 55, 55]) -> None:
        super().__init__()
        self.title: str = str(title)
        self.size: list[int] = [*map(int, size)]
        self.color: list[int] = [*map(int, color)]
        self.aspect: float = self.size[0] / self.size[1]
        self.raster: pg.Surface = pg.display.set_mode(self.size)
        self.icon: pg.Surface = pg.image.load(miniform.utils._miniform_path("assets/images/icon.png"))

        pg.display.set_caption(self.title)
        pg.display.set_icon(self.icon)

    def set_title(self, title: str) -> None:
        if isinstance(title, str):
            self.title = title
            pg.display.set_caption(self.title)

    def set_icon(self, icon: pg.Surface) -> None:
        if isinstance(icon, pg.Surface):
            self.icon = icon
            pg.display.set_icon(self.icon)

    def clear(self) -> None:
        self.raster.fill(self.color)

    def update(self) -> None:
        pg.display.update()
    
    def draw(self, surface: pg.Surface, pos: list[int]) -> None:
        self.raster.blit(surface, pos)
