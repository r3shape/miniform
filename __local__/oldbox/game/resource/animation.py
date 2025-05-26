from oldbox.globs import pg
from oldbox.atom import Atom

# ------------------------------------------------------------ #
class Animation(Atom):
    def __init__(
            self, surfmap,
            path: str,
            frame_size: list[int],
            frame_layout: list[int],
            loop: bool=True,
            speed: float=5.0
        ) -> None:
        super().__init__(surfmap.load_surface(frame_size, path, frame_layout), 0)
        self.surfmap = surfmap
        self.index = 0
        self.timer = 0.0
        self.loop = loop
        self.done = False
        self.speed = 1 / speed
        self.size = frame_size
        self.frame_layout = frame_layout
        self.frame_count = frame_layout[0] * frame_layout[1]

    @property
    def frame_data(self) -> list[int]:
        columns, rows = self.frame_layout
        frame_x = (self.index % columns) * self.size[0]
        frame_y = (self.index // columns) * self.size[1]
        return [frame_x, frame_y]

    def reset(self) -> None:
        self.timer = 0.0
        self.index = 0
        self.done = False

    def copy(self):
        return Animation(self.surfmap, self.path, self.frame_count, self.size, self.loop, self.speed)

    def update(self, delta_time: float) -> None:
        if self.done: return
        self.timer += delta_time
        if self.timer >= self.speed:
            self.timer = 0
            self.index += 1
            if self.index >= self.frame_count:
                if self.loop:
                    self.index = 0
                else:
                    self.index = self.frame_count - 1
                    self.done = True
# ------------------------------------------------------------ #
