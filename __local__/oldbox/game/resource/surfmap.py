from oldbox.globs import os, pg
from oldbox.game.obj import Object
from oldbox.app.window import Window
from oldbox.util import add_v2, mul_v2

# ------------------------------------------------------------ #
class SurfMap(Object):
    def __init__(self, size: list[int]) -> None:
        super().__init__([0, 0], size, [1, 1, 1])
        self.set_colorkey([1, 1, 1])
        self.fill()
        self.padding: list[int] = [0, 0]
        self.surf_data: list[tuple[list[int], list[int]]] = []

    def load_surface(self, size: list[int], path: str, frame_layout: list[int]=[1, 1]) -> int:
        if not os.path.exists(path): return
        surfid = len(self.surf_data)

        surface = pg.image.load(path).convert_alpha()
        w, h = mul_v2(size, frame_layout)
        if self.pos[0] + w >= self.size[0]:
            self.pos[0] = 0
            if self.pos[1] + h + self.surf_data[surfid-1][1][1] > self.size[1]: return
            for p, s in self.surf_data:
                if h < s[1]:
                    h = s[1]
            self.pos[1] += h

        self.image.blit(surface, self.pos)
        del surface

        self.surf_data.append([self.pos[:], size[:]])
        self.pos[0] += w
        return surfid

    def unload_surface(self, surfid: int) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        pos, size = self.surf_data[surfid]
        surface = pg.Surface(size)
        surface.fill([1, 1, 1])
        self.image.blit(surface, pos, pg.Rect(pos, size))

    def blit(self, surfid: int, surface: pg.Surface, pos: list[int], offset: list[int]=[0, 0], frame_data: list[int]=[0, 0]) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        blit_pos = add_v2(pos, offset)
        src_pos, src_size = self.surf_data[surfid]
        src_rect = pg.Rect(add_v2(src_pos, frame_data), src_size)
        surface.blit(self.image, blit_pos, src_rect)
# ------------------------------------------------------------ #
