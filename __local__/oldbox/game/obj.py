from oldbox.globs import pg
from oldbox.util import mag_v2, div_v2, sub_v2, clamp, add_v2, damp_lin

from oldbox.atom import Atom

# ------------------------------------------------------------ #
class Object(Atom):
    def __init__(
            self,
            pos: list[int]=[0, 0],
            size: list[int]=[32, 32],
            color: list[int]=[255, 255, 255],
            bounds: list[int]=None, mass: float=100) -> None:
        super().__init__(0, 0)
        self.cell = 0
        self.pos = pos
        self.size = size
        self.mass = mass
        self.color = color
        self.velocity = [0, 0]
        self.minvelocity = 5.0

        self.image = pg.Surface(size)
        self.bounds = bounds[:] if bounds else None
        self.fill()

    @property
    def center(self) -> list[float]:
        return add_v2(self.pos, div_v2(self.size, 2))
    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)
    @property
    def dx(self) -> int:
        return ((self.velocity[0] > 0) - (self.velocity[0] < 0))
    @property
    def dy(self) -> int:
        return ((self.velocity[1] > 0) - (self.velocity[1] < 0))

    def fill(self) -> None:
        self.image.fill(self.color)
    
    def set_colorkey(self, color: list[int]) -> None:
        self.image.set_colorkey(color)

    def set_velocity(self, vx: float=0.0, vy: float=0.0) -> None:
        self.velocity[0] = vx if vx else self.velocity[0]
        self.velocity[1] = vy if vy else self.velocity[1]

    def _aabbx(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect
        for obj in collidables:
            if rect.colliderect(obj.rect):
                if transform[0] < 0:
                    rect.left = obj.rect.right
                    self.velocity[0] = 0
                if transform[0] > 0:
                    rect.right = obj.rect.left
                    self.velocity[0] = 0
                self.pos[0] = rect.x
    
    def _aabby(self, transform: list[float], collidables: list["Object"]) -> None:
        rect = self.rect
        for obj in collidables:
            if rect.colliderect(obj.rect):
                if transform[1] < 0:
                    rect.top = obj.rect.bottom
                    self.velocity[1] = 0
                if transform[1] > 0:
                    rect.bottom = obj.rect.top
                    self.velocity[1] = 0
                self.pos[1] = rect.y

    def update(self, dt: float, collidables: list) -> None:
        transform = [((self.velocity[0] > 0) - (self.velocity[0] < 0)) + self.velocity[0],
                     ((self.velocity[1] > 0) - (self.velocity[1] < 0)) + self.velocity[1]]

        self.pos[0] += transform[0] * dt
        self._aabbx(transform, collidables)

        self.pos[1] += transform[1] * dt
        self._aabby(transform, collidables)

        self.velocity = [*map(lambda v: damp_lin(v, self.mass, self.minvelocity, dt), self.velocity)]
# ------------------------------------------------------------ #