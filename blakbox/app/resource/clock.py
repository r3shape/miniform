from blakbox.globs import pg, time
from blakbox.atom import BOXatom

# ------------------------------------------------------------ #
class BOXclock(BOXatom):
    def __init__(self, fps: float=60):
        super().__init__(0, 0)
        self._ = pg.time.Clock()
        self.fps: float = 0.0
        self.tfps: float = fps
        self.delta: float = 0.0
        self.time: float = time.time()
        self.start: float = time.time()

    def tick(self) -> None:
        self.delta = time.time() - self.time  # update dt
        self.time = time.time()               # update t
        self.fps = self._.get_fps()           # update fps
    
    def rest(self) -> None:
        self._.tick(self.tfps)
# ------------------------------------------------------------ #