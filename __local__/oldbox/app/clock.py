from oldbox.globs import pg, time
from oldbox.atom import Atom

# ------------------------------------------------------------ #
class Clock(Atom):
    def __init__(self, fps: float=60):
        super().__init__(0, 0)
        self._ = pg.time.Clock()
        self.data = [time.time(), time.time(), 0, 0, fps]    # t s dt fps tfps
    
    @property
    def fps(self) -> float:     return self.data[3]
    @property
    def start(self) -> float:   return self.data[1]
    @property
    def delta(self) -> float:   return self.data[2]
    @property
    def current(self) -> float: return self.data[0]

    def tick(self) -> None:
        self.data[2] = time.time() - self.data[0]  # update dt
        self.data[0] = time.time()                 # update t
        self.data[3] = self._.get_fps()            # update fps
    
    def rest(self) -> None:
        self._.tick(self.data[4])
# ------------------------------------------------------------ #

