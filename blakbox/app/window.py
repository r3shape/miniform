from blakbox.globs import pg
from blakbox.util import add_v2, div_v2, scale_v2, clamp

from blakbox.atom import Atom

# ------------------------------------------------------------ #
class Window(Atom):
    def __init__(
            self,
            screen_size: list[int],
            display_size: list[int],
            clip_range: list[int],
            clear_color: list[int],
            ) -> None:
        super().__init__(0, 0)
        self.zoom: float = 1.0
        self.icon: pg.Surface = None
        self.title: str = "BlakWindow"
        self.display = pg.Surface(display_size)
        self.clip_range: list[int] = clip_range[:]
        self.clear_color: list[int] = clear_color[:]
        self.screen_size: list[int] = screen_size[:]
        self.display_size: list[int] = display_size[:]
        self.screen = pg.display.set_mode(screen_size)

    def mod_icon(self, icon: pg.Surface) -> None:
        if not isinstance(icon, pg.Surface): return
        self.icon = icon
        pg.display.set_icon(self.icon)

    def mod_title(self, title: str) -> None:
        if not isinstance(title, str): return
        self.title = title
        pg.display.set_caption(title)

    def mod_display(self, display_size: list[int]) -> None:
        self.display_size = display_size
        self.display = pg.Surface(display_size)

    def mod_zoom(self, delta: float) -> None:
        self.zoom = clamp(self.zoom + delta, 1, 3.5)
    
    def fill(self) -> None:
        self.screen.fill(self.clear_color)
        self.display.fill(self.clear_color)

    def _rad_clip(self, pos: list[float], offset: list[float], radius: float = 0) -> bool:
        pos = add_v2(pos, offset)
        return ((pos[0] + radius < self.clip_range[0])               or
                (pos[0] + self.clip_range[0] > self.display_size[0]) or
                (pos[1] + radius < self.clip_range[1])               or
                (pos[0] + self.clip_range[1] > self.display_size[1]))

    def _blit_clip(self, pos: list[float], size: list[int], offset: list[float]) -> bool:
        pos = add_v2(add_v2(pos, div_v2(size, 2)), offset)
        return ((pos[0] - self.clip_range[0]) < 0 or pos[0] + self.clip_range[0] > self.display_size[0]\
             or (pos[1] - self.clip_range[1]) < 0 or pos[1] + self.clip_range[1] > self.display_size[1])

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

    def blitr(self, rect: pg.Rect, offset: list[float]=[0, 0], color: list[int]=[255, 255, 255], width: int=1) -> None:
        self.draw_rect(rect.topleft, rect.size, offset, color, width)

    def blit(self, surface: pg.Surface, pos: list[int], offset: list[int]=[0, 0], rect: pg.Rect=None) -> None:
        if self._blit_clip(pos, surface.size, offset): return
        self.display.blit(surface, add_v2(pos, offset), rect)

    def update(self) -> None:
        pg.display.flip()
# ------------------------------------------------------------ #
