from r3frame.globs import pg
from r3frame.atom import Atom
from r3frame.util import mag_v2, div_v2, sub_v2, clamp

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
        self.data = [
            size[:], color[:], pg.Surface(size),
            100, pos[:], [0, 0, 0, 0, None, bounds[:] if bounds is not None else None]] 
        """ `Object` data array: [size, color, surface, speed, pos, movement[left, right, up, down, move_to, bounds]] """
        self.fill()

    @property
    def size(self) -> list[int]:        return self.data[0]
    @property
    def color(self) -> list[int]:       return self.data[1]
    @property
    def image(self) -> pg.Surface:      return self.data[2]
    @property
    def speed(self) -> float:           return self.data[3]
    @property
    def pos(self) -> list[float]:       return self.data[4]
    @property
    def movement(self) -> list[bool]:   return self.data[5]
    @property
    def bounds(self) -> float:          return self.data[5][5]
    @property
    def colorkey(self) -> None: return self.data[2].get_colorkey()
    @property
    def center(self) -> list[float]:
        return [self.data[4][0] + (self.data[0][0] / 2),
                self.data[4][1] + (self.data[0][1] / 2)]
    
    def fill(self) -> None:
        self.data[2].fill(self.data[1])
    
    def mod_color(self, color: list[int]) -> None:
        self.data[1] = color[:]
    
    def mod_colorkey(self, color: list[int]) -> None:
        self.data[2].set_colorkey(color)
    
    def mod_bounds(self, bounds: list[int]) -> None:
        self.data[5][5][0] = bounds[0]
        self.data[5][5][1] = bounds[1]

    def rect(self) -> pg.Rect:
        return pg.Rect(self.data[4], self.data[0])
    
    def move_to(self, pos: list[float]) -> None:
        self.data[5][4] = pos[:] if pos else None

    def move(self, l: bool=None, r: bool=None, u: bool=None, d: bool=None) -> None:
        self.data[5][0] = True if l else False
        self.data[5][1] = True if r else False
        self.data[5][2] = True if u else False
        self.data[5][3] = True if d else False
    
    def _aabbx(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[0] < 0:
                    rect.left = obj.rect().right
                    self.data[5][0] = 0
                if transform[0] > 0:
                    rect.right = obj.rect().left
                    self.data[5][1] = 0
                self.data[4][0] = rect.x
    
    def _aabby(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[1] < 0:
                    rect.top = obj.rect().bottom
                    self.data[5][2] = 0
                if transform[1] > 0:
                    rect.bottom = obj.rect().top
                    self.data[5][3] = 0
                self.data[4][1] = rect.y

    def update(self, dt: float, collidables: list["Object"]=[]) -> None:
        if self.data[5][4]:
            diff = sub_v2(self.data[5][4], self.center)
            dist = mag_v2(diff)
            if int(dist) <= 8:
                self.data[5][4] = None
            else:
                dirt = div_v2(diff, dist)
                if self.data[5][5]:
                    self.data[4][0] = clamp(self.data[4][0] + dirt[0] * self.data[3] * dt, 0, self.data[5][5][0])
                    self._aabbx(dirt, collidables)
                    self.data[4][1] = clamp(self.data[4][1] + dirt[1] * self.data[3] * dt, 0, self.data[5][5][1])
                    self._aabby(dirt, collidables)
                else:
                    self.data[4][0] += dirt[0] * self.data[3] * dt
                    self._aabbx(dirt, collidables)
                    self.data[4][1] += dirt[1] * self.data[3] * dt
                    self._aabby(dirt, collidables)
        else:        
            t = [(self.data[5][1] - self.data[5][0]) * self.data[3],
                (self.data[5][3] - self.data[5][2]) * self.data[3]]
            if self.data[5][5]:
                self.data[4][0] = clamp(self.data[4][0] + t[0] * dt, 0, self.data[5][5][0])
                self._aabbx(t, collidables)
                self.data[4][1] = clamp(self.data[4][1] + t[1] * dt, 0, self.data[5][5][1])
                self._aabby(t, collidables)
            else:
                self.data[4][0] += t[0] * dt
                self._aabbx(t, collidables)
                self.data[4][1] += t[1] * dt
                self._aabby(t, collidables)
# ------------------------------------------------------------ #