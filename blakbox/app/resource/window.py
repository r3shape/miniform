from blakbox.globs import pg
from blakbox.atom import BOXatom
from blakbox.util import add_v2, sub_v2, div_v2, abs_path

# ------------------------------------------------------------ #
class BOXwindow(BOXatom):
    def __init__(
            self,
            title: str = "BOXwindow",
            clip_range: list[int] = [1, 1],
            screen_size: list[int] = [800, 600],
            display_size: list[int] = [1600, 1200],
            clear_color: list[int] = [25, 25, 25],
            ) -> None:
        super().__init__(0, 0)
        self.title: str = title
        self.icon: pg.Surface = pg.image.load(abs_path("assets/images/logo.ico"))

        self.clip_range: list[int] = clip_range[:]
        self.clear_color: list[int] = clear_color[:]
        self.screen_size: list[int] = screen_size[:]
        self.screen = pg.display.set_mode(screen_size)
        self.screen.fill(clear_color)
        self.aspect_ratio: int = int(self.screen_size[1] / self.screen_size[0])

        self.display_size: list[int] = display_size[:]
        self.display = pg.Surface(display_size, pg.SRCALPHA)
        self.display.fill(clear_color)

        self.mod_title(self.title)
        self.mod_icon(self.icon)

    def mod_icon(self, surface: pg.Surface) -> None:
        if not isinstance(surface, pg.Surface): return
        pg.display.set_icon(surface)
        self.icon = surface

    def mod_title(self, title: str) -> None:
        if not isinstance(title, str): return
        pg.display.set_caption(title)
        self.title = title

    def mod_display(self, display_size: list[int]) -> None:
        self.display_size = display_size
        self.display = pg.Surface(display_size)

    def fill(self) -> None:
        self.screen.fill(self.clear_color)
        self.display.fill(self.clear_color)

    def _rad_clip(self, pos: list[float], offset: list[float], radius: float = 0) -> bool:
        pos = add_v2(pos, offset)
        return ((pos[0] + radius < self.clip_range[0])               or
                (pos[0] > self.display_size[0]) or
                (pos[1] + radius < self.clip_range[1])               or
                (pos[1] > self.display_size[1]))

    def _blit_clip(self, pos: list[float], size: list[int], offset: list[float]) -> bool:
        pos = add_v2(pos, offset)
        return ((pos[0] + size[0]) < self.clip_range[0] or pos[0] > self.display_size[0]\
            or  (pos[1] + size[1]) < self.clip_range[1] or pos[1] > self.display_size[1])

    def draw_line(
            self, 
            start: list[float],
            end: list[float],
            offset: list[float]=[0, 0],
            color: list[float]=[255, 255, 255], width: int=1) -> None:
        if self._rad_clip(start, offset, 0) or self._rad_clip(end, offset, 0): return
        pg.draw.line(self.display, color, add_v2(start, offset), add_v2(end, offset), width=width)

    def draw_rect(
        self, 
        pos: list[float],
        size: list[float],
        offset: list[float]=[0, 0],
        color: list[float]=[255, 255, 255], width: int=1) -> None:
        if self._blit_clip(pos, size, offset): return
        pg.draw.rect(self.display, color, pg.Rect(add_v2(pos, offset), size), width=width)

    def draw_circle(
        self,
        radius: float,
        center: list[int],
        offset: list[float]=[0, 0],
        color: list[int]=[255, 255, 255], width: int=1) -> None:
        if self._rad_clip(center, offset, radius): return
        pg.draw.circle(self.display, color, add_v2(center, offset), radius, width)

    def blit(self, obj, offset: list[float] = [0.0, 0.0], rect: pg.Rect=None) -> None:
        if self._blit_clip(obj.pos, obj.size, offset): return
        self.display.blit(obj.surface, rect if rect else add_v2(obj.pos, offset))
    
    def blits(self, surface: pg.Surface, pos: list[int], offset: list[int]=[0.0, 0.0], rect: pg.Rect=None) -> None:
        if self._blit_clip(pos, surface.size, offset): return
        self.display.blit(surface, rect if rect else add_v2(pos, offset))
    
    def blitr(self, rect: pg.Rect, offset: list[float]=[0, 0], color: list[int]=[255, 255, 255], width: int=1) -> None:
        if self._blit_clip(rect.topleft, rect.size, offset): return
        self.draw_rect(rect.topleft, rect.size, offset, color, width)

    def update(self) -> None:
        pg.display.flip()
# ------------------------------------------------------------ #