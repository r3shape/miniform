from r3frame.globs import pg
from r3frame.util import damp_lin

class Object:
    def __init__(self, size: list[int]=[32, 32], color: list[int]=[255, 255, 255], location: list[int]=[0, 0], mass: float=100, image_offset: list[int]=[0, 0]) -> None:
        self.id = "obj"
        self.cell = 0
        self.mass = mass
        self.size = size
        self.color = color
        self.velocity = [0, 0]
        self.minvelocity = 5.0
        self.location = location
        self.collisions = [0, 0, 0, 0]   # l, r, u, d

        self._image = pg.Surface(size)
        self._image.fill(color)

        self.image = self._image
        self.image_offset = image_offset

    def set_color(self, color: list[int]) -> None:
        self.color = color
        self._image.fill(color)
        self.image = self._image

    def rect(self) -> pg.Rect:
        return pg.Rect(self.location, self.size)

    def center(self) -> list[float]:
        return [
            self.location[0] + (self.size[0] / 2),
            self.location[1] + (self.size[1] / 2)
        ]

    def render(self, window) -> None:
        window.blit(self.image, [
            self.location[0] + self.image_offset[0],
            self.location[1] + self.image_offset[1]
        ])

    def set_velocity(self, vx: float=0.0, vy: float=0.0) -> None:
        self.velocity[0] = vx if vx else self.velocity[0]
        self.velocity[1] = vy if vy else self.velocity[1]

    def update(self, collidables: list, delta_time: float) -> None:
        self.collisions = [0, 0, 0, 0]   # l, r, u, d
        transform = [
            ((self.velocity[0] > 0) - (self.velocity[0] < 0)) + self.velocity[0],
            ((self.velocity[1] > 0) - (self.velocity[1] < 0)) + self.velocity[1]
        ]

        self.location[0] += transform[0] * delta_time
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[0] < 0:
                    rect.left = obj.rect().right
                    self.velocity[0] = 0
                    self.collisions[0] = 1
                if transform[0] > 0:
                    rect.right = obj.rect().left
                    self.velocity[0] = 0
                    self.collisions[1] = 1
                self.location[0] = rect.x

        self.location[1] += transform[1] * delta_time
        rect = self.rect()
        for obj in collidables:
            if rect.colliderect(obj.rect()):
                if transform[1] < 0:
                    rect.top = obj.rect().bottom
                    self.velocity[1] = 0
                    self.collisions[2] = 1
                if transform[1] > 0:
                    rect.bottom = obj.rect().top
                    self.velocity[1] = 0
                    self.collisions[3] = 1
                self.location[1] = rect.y

        self.velocity = [*map(lambda v: damp_lin(v, self.mass, self.minvelocity, delta_time), self.velocity)]
