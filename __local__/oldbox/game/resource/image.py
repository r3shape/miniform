from oldbox.globs import os, pg
from oldbox.atom import Atom
from oldbox.util import equal_arrays
from oldbox.app.window import Window

# ------------------------------------------------------------ #
class Image(Atom):
    def __init__(self, surfmap, path: str, size: list[int], color: list[int] = [255, 255, 255]) -> None:
        super().__init__(surfmap.load_surface(size, path), 0)
        self.surfmap = surfmap
        self.path: str = path
        self.color: list[int] = color
        self.rotation: float = 0.0
        self.scale: list[float] = [1.0, 1.0]
        self.size: list[int] = size[:]  # now passed in manually (you have to know the frame size)
        
    @property
    def frame_data(self) -> list[int]:
        # simple, static image, always just use (0,0)
        return [0, 0]

    def fill(self, color: list[int] = None) -> None:
        if not isinstance(color, list): return
        if equal_arrays(self.color, color): return

        pos, size = self.surfmap.surf_data[self.id]
        surface = pg.Surface(size, pg.SRCALPHA)
        surface.fill(color if color else self.color)
        self.surfmap.image.blit(surface, pos, pg.Rect(pos, size))
        self.color = color if color else self.color

    def set_scale(self, scale: list[float]) -> None:
        if not isinstance(scale, list): return
        if equal_arrays(self.scale, scale): return

        # NOTE: scaling *at runtime* for surfmap images is tricky.
        # Instead, store scale and apply at render time if needed
        self.scale = scale
# ------------------------------------------------------------ #
