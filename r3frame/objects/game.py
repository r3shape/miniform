from r3frame.globals import pg
from r3frame.utils import damp_lin

class Game_Object():
    def __init__(self, size=[32, 32], color=[0, 255, 0], location=[0, 0]):
        self.size = size
        self.color = color
        self.image = pg.Surface(size)
        self.image.fill(color)
        self.location = location
        self.last_location = location
        self.velocity = [0.0, 0.0]
        
    def get_rect(self) -> pg.Rect: return pg.Rect(self.location, self.size)

    def set_image(self, image: pg.Surface) -> None:
        if isinstance(image, pg.Surface):
            self.image = image
        elif isinstance(image, None):
            self.image = pg.Surface(self.size)
            self.image.fill(self.color)

    def set_velocity(self, vx: float=0.0, vy: float=0.0) -> None:
        if vx: self.velocity[0] = vx
        if vy: self.velocity[1] = vy

    def update(self, delta_time: float) -> None:
        # Apply movement
        self.last_location = self.location
        self.location[0] += self.velocity[0] * delta_time
        self.location[1] += self.velocity[1] * delta_time
        self.velocity = [*map(lambda v: damp_lin(v, 100, 1, delta_time), self.velocity)]
