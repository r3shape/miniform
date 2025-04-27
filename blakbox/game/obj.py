from blakbox.globs import pg
from blakbox.util import mag_v2, div_v2, sub_v2, clamp, add_v2

from blakbox.atom import Atom

# ------------------------------------------------------------ #
class Object(Atom):
    def __init__(
            self,
            pos: list[int],
            size: list[int],
            color: list[int],
            bounds: list[int]=None,
    ) -> None:
        super().__init__(0, 0)
        self.size = size[:]
        self.color = color[:]
        self.image = pg.Surface(size)
        
        self.speed = 100
        self.pos = pos[:]
        self.movement = [0, 0, 0, 0, None]
        self.bounds = bounds[:] if bounds else None
        self.fill()
    
    @property
    def center(self) -> list[float]:
        return add_v2(self.pos, div_v2(self.size, 2))
    
    def fill(self) -> None:
        self.image.fill(self.color)
    
    def mod_colorkey(self, color: list[int]) -> None:
        self.image.set_colorkey(color)
    
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)
    
    def move_to(self, pos: list[float]) -> None:
        self.movement[4] = pos[:] if pos else None

    def move(self, l: bool=None, r: bool=None, u: bool=None, d: bool=None) -> None:
        self.movement[0] = True if l else False
        self.movement[1] = True if r else False
        self.movement[2] = True if u else False
        self.movement[3] = True if d else False
    
    def _aabbx(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[0] < 0:
                    rect.left = obj.rect().right
                    self.movement[0] = 0
                if transform[0] > 0:
                    rect.right = obj.rect().left
                    self.movement[1] = 0
                self.pos[0] = rect.x
    
    def _aabby(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[1] < 0:
                    rect.top = obj.rect().bottom
                    self.movement[2] = 0
                if transform[1] > 0:
                    rect.bottom = obj.rect().top
                    self.movement[3] = 0
                self.pos[1] = rect.y

    def update(self, dt: float, collidables: list["Object"]=[]) -> None:
        if self.movement[4]:
            diff = sub_v2(self.movement[4], self.center)
            dist = mag_v2(diff)
            if int(dist) <= 8:
                self.movement[4] = None
            else:
                dirt = div_v2(diff, dist)
                if self.bounds:
                    self.pos[0] = clamp(self.pos[0] + dirt[0] * self.speed * dt, 0, self.bounds[0])
                    self._aabbx(dirt, collidables)
                    self.pos[1] = clamp(self.pos[1] + dirt[1] * self.speed * dt, 0, self.bounds[1])
                    self._aabby(dirt, collidables)
                else:
                    self.pos[0] += dirt[0] * self.speed * dt
                    self._aabbx(dirt, collidables)
                    self.pos[1] += dirt[1] * self.speed * dt
                    self._aabby(dirt, collidables)
        else:        
            t = [(self.movement[1] - self.movement[0]) * self.speed,
                 (self.movement[3] - self.movement[2]) * self.speed]
            if self.bounds:
                self.pos[0] = clamp(self.pos[0] + t[0] * dt, 0, self.bounds[0])
                self._aabbx(t, collidables)
                self.pos[1] = clamp(self.pos[1] + t[1] * dt, 0, self.bounds[1])
                self._aabby(t, collidables)
            else:
                self.pos[0] += t[0] * dt
                self._aabbx(t, collidables)
                self.pos[1] += t[1] * dt
                self._aabby(t, collidables)
# ------------------------------------------------------------ #