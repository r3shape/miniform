from blakbox.globs import pg
from blakbox.app.resource.base import Resource

# ------------------------------------------------------------ #
class Animation(Resource):
    def __init__(
            self,
            rid: int,
            frames: list[pg.Surface],
            loop: bool=1, frame_duration: float=5.0,
            frame_offset: list[int]=[0, 0]
        ) -> None:
        super().__init__(rid, frames)
        self.done = 0
        self.frame = 0
        self.loop = loop
        self.flip_x = False
        self.flip_y = False
        self.frame_offset = frame_offset
        self.frame_duration = frame_duration

    def reset(self) -> None: self.frame, self.done = 0, 0

    def copy(self):
        return Animation(self.data, self.loop, self.frame_duration, self.frame_offset)

    def get_frame(self):
        return pg.transform.flip(self.data[int(self.frame / self.frame_duration)].data, self.flip_x, self.flip_y)

    def update(self) -> None:
        if self.loop:
            self.frame = (self.frame + 1) % (self.frame_duration * len(self.data))
        else:
            self.frame = min(self.frame + 1, self.frame_duration * len(self.data) - 1)
            if self.frame >= self.frame_duration * len(self.data) - 1:
                self.done = 1
# ------------------------------------------------------------ #
