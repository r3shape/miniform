from blakbox.globals import pg
from blakbox.atom import BOXatom
from blakbox.resource.surfatlas import BOXsurfatlas

# ------------------------------------------------------------ #
class BOXsurfarray(BOXatom):
    def __init__(
            self,
            atlas_id: int,
            atlas_tag: str,
            path: str,
            size: list[int],
            layout: list[int],
            loop: bool=True,
            speed: float=5.0
        ) -> None:
        super().__init__(atlas_id, 0)
        self.atlas_tag: str = atlas_tag
        self.index = 0
        self.timer = 0.0
        self.loop = loop
        self.done = False
        self.speed = 1 / speed
        self.size = size
        self.layout = layout
        self.count = layout[0] * layout[1]

    @property
    def data(self) -> list[int]:
        columns, rows = self.layout
        frame_x = (self.index % columns) * self.size[0]
        frame_y = (self.index // columns) * self.size[1]
        return [frame_x, frame_y]

    def reset(self) -> None:
        self.timer = 0.0
        self.index = 0
        self.done = False

    def copy(self):
        return BOXsurfarray(self.path, self.size, self.layout, self.atlas, self.loop, self.speed)

    def update(self, dt: float) -> None:
        if self.done: return
        self.timer += dt
        if self.timer >= self.speed:
            self.timer = 0
            self.index += 1
            if self.index >= self.count:
                if self.loop:
                    self.index = 0
                else:
                    self.index = self.count - 1
                    self.done = True
# ------------------------------------------------------------ #
