from miniform.imports import pg, time
import miniform

class MiniClock(miniform.MiniAtom):
    def __init__(self, rate: float, target: float = 60.0) -> None:
        super().__init__()
        self.tick: bool = 0             # in seconds
        self.fps: float = 0.0
        self.rate: float = rate
        self.delta: float = 0.0
        self.target: float = target
        self.now: float = time.time()
        self._last_tick: float = time.time()
        self._internal: pg.Clock = pg.Clock()

    def update(self) -> None:
        was = self.now
        self.now = time.time()
        self.delta = self.now - was

        if self.now - self._last_tick >= self.rate:
            self.tick = 1
            self._last_tick = self.now
        else:
            self.tick = 0

        self.fps = self._internal.get_fps()
        self._internal.tick(self.target)
