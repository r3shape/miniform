from r3frame.globs import os, pg
from r3frame.atom import Atom
from r3frame.util import equal_arrays
from r3frame.app.window import Window
from r3frame.app.resource.base import Resource

# ------------------------------------------------------------ #
class Image(Resource):
    def __init__(self, rid: int, path: str, data: pg.Surface, color: list[int]=[255, 255, 255]) -> None:
        super().__init__(rid, data)
        self.path: str = path
        self.rotation: float = 0.0
        self.color: list[int] = color
        self.scale: list[float] = [1.0, 1.0]
        self.size: list[int] = [self.data.get_width(), self.data.get_height()]

    def fill(self, color: list[int]=None) -> None:
        if not isinstance(color, list): return
        if equal_arrays(self.color, color): return
        self.data.fill(color if color else self.color)
        self.color = color if color else self.color

    def set_scale(self, scale: list[float]) -> None:
        if not isinstance(scale, list): return
        if equal_arrays(self.scale, scale): return
        self.data = pg.transform.scale(self.data, [
            self.size[0] * scale[0],
            self.size[1] * scale[1]
        ])
        self.scale = scale
# ------------------------------------------------------------ #


# ------------------------------------------------------------ #
class TextureConfig:
    def __init__(self, path: str, sizep: list[int]) -> None:
        self.path: str = path
        self.sizep: list[int] = sizep

class Atlas(Atom):
    def __init__(self, sizep: list[int]) -> None:
        super().__init__(0, 0)
        self.sizep: list[int] = sizep[:]
        self.location: list[int] = [0, 0]
        self.surface: pg.Surface = pg.Surface(sizep)
        self.surface.set_colorkey([1, 1, 1])
        self.surface.fill([1, 1, 1])
        self.data: list[tuple[str, list[int], list[int]]] = []

    def load_texture(self, config: TextureConfig) -> None:
        if not isinstance(config, TextureConfig): return
        if not os.path.exists(config.path): return
        tid = len(self.data)

        image = pg.image.load(config.path).convert_alpha()
        w, h = config.sizep

        if self.location[0] + w > self.sizep[0]:
            self.location[0] = 0
            self.location[1] += h

        if self.location[1] + h > self.sizep[1]: return

        self.surface.blit(image, self.location)
        del image

        self.data.append(([w, h], self.location[:]))
        self.location[0] += w  # move right for next texture

        return tid

    def unload_texture(self, tid: int) -> None:
        if tid < 0 or tid >= len(self.data): return
        
        size, location = self.data[tid]
        rect = pg.Rect(location, size)
        surface = pg.Surface(size)
        surface.fill([1, 1, 1])
        
        self.surface.blit(surface, location, rect)

    def blit_texture(self, tid: int, window: Window, blit_location: list[int], offset: list[int]=[0, 0]) -> None:
        if tid < 0 or tid >= len(self.data): return
        size, location = self.data[tid]
        rect = pg.Rect(location, size)
        window.blit(self.surface, blit_location, size, offset, rect)
# ------------------------------------------------------------ #
