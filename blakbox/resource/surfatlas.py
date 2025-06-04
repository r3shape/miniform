from blakbox.globals import os, pg
from blakbox.utils import add_v2, mul_v2
from blakbox.resource.object import BOXobject

# ------------------------------------------------------------ #
class BOXsurfatlas(BOXobject):
    def __init__(self, size: list[int]) -> None:
        super().__init__(size=size, color=[1, 1, 1])
        self.set_colorkey([1, 1, 1])
        self.set_color([1, 1, 1], True)
        self.padding: list[int] = [0, 0]
        self.surf_data: list[tuple[list[int], list[int]]] = []

    def load_surface(self, size: list[int], path: str, frame_layout: list[int]=[1, 1]) -> int:
        if not os.path.exists(path): return
        surfid = len(self.surf_data)

        surface = pg.image.load(path).convert_alpha()
        width, height = mul_v2(size, frame_layout)
        if self.pos[0] + width >= self.size[0]:
            self.pos[0] = 0
            if self.pos[1] + height + self.surf_data[surfid-1][1][1] > self.size[1]: return
            for p, s in self.surf_data:
                if height < s[1]:
                    height = s[1]
            self.pos[1] += height

        self.surface.blit(surface, self.pos)
        del surface

        self.surf_data.append([self.pos[:], size[:]])
        self.pos[0] += width
        return surfid

    def unload_surface(self, surfid: int) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        pos, size = self.surf_data[surfid]
        surface = pg.Surface(size)
        surface.fill([1, 1, 1])
        self.surface.blit(surface, pos, pg.Rect(pos, size))

    def blit(self, surfid: int, surface: pg.Surface, pos: list[int], offset: list[int]=[0, 0], data: list[int]=[0, 0], rect: pg.Rect = None) -> None:
        if surfid < 0 or surfid >= len(self.surf_data): return
        blit_pos = add_v2(pos, offset)
        src_pos, src_size = self.surf_data[surfid]

        if rect is None:
            src_rect = pg.Rect(add_v2(src_pos, data), src_size)
        else: src_rect = rect
        
        surface.blit(self.surface, blit_pos, src_rect)
# ------------------------------------------------------------ #
