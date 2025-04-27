from blakbox.util import add_v2
from blakbox.globs import os, pg
from blakbox.game.obj import Object
from blakbox.app.window import Window

# ------------------------------------------------------------ #
class SurfMap(Object):
    def __init__(self, size: list[int]) -> None:
        super().__init__([0, 0], size, [1, 1, 1])
        self.mod_colorkey([1, 1, 1])
        self.fill()
        self.surf_data: list[tuple[list[int], list[int]]] = []

    def load_surface(self, size: list[int], path: str) -> int:
        if not os.path.exists(path): return
        surfid = len(self.surf_data)

        surface = pg.image.load(path).convert_alpha()
        w, h = size
        if self.pos[0] + w > self.size[0]:
            self.pos[0] = 0
            self.pos[1] += h

        if self.pos[1] + h > self.size[1]: return

        self.image.blit(surface, self.pos)
        del surface

        self.surf_data.append([self.pos[:], size[:]])
        self.pos[0] += w  # move right for next texture

        return surfid

    def unload_surface(self, surfid: int) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        pos, size = self.surf_data[surfid]
        surface = pg.Surface(size)
        surface.fill([1, 1, 1])
        self.image.blit(surface, pos, pg.Rect(pos, size))

    def blit(self, surfid: int, surface: pg.Surface, pos: list[int], offset: list[int]=[0, 0]) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        pos = add_v2(pos, offset)
        surface.blit(self.image, pos, pg.Rect(*self.surf_data[surfid]))
# ------------------------------------------------------------ #
