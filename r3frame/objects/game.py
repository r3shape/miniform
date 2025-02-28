from r3frame.globals import pg
from r3frame.utils import damp_lin

# ------------------------------------------------------------ #
class Animation:
    def __init__(self, frames: list[pg.Surface], loop: bool=1, frame_duration: float=5.0, frame_offset: list[int]=[0, 0]) -> None:
        self.done = 0
        self.frame = 0
        self.loop = loop
        self.flip_x = False
        self.flip_y = False
        self.frames = frames
        self.frame_offset = frame_offset
        self.frame_duration = frame_duration

    def reset(self) -> None: self.frame, self.done = 0, 0

    def copy(self):
        return Animation(self.frames, self.loop, self.frame_duration, self.frame_offset)

    def get_frame(self):
        return pg.transform.flip(self.frames[int(self.frame / self.frame_duration)], self.flip_x, self.flip_y)

    def update(self) -> None:
        if self.loop:
            self.frame = (self.frame + 1) % (self.frame_duration * len(self.frames))
        else:
            self.frame = min(self.frame + 1, self.frame_duration * len(self.frames) - 1)
            if self.frame >= self.frame_duration * len(self.frames) - 1:
                self.done = 1
# ------------------------------------------------------------ #

# ------------------------------------------------------------ #
class Game_Object:
    def __init__(self, size: list[int]=[32, 32], color: list[int]=[0, 255, 0], location: list[int]=[0, 0], mass: float=100.0, speed: float=100.0, vthreshold: float=5.0):
        self.size = size
        self.color = color
        self.image = pg.Surface(size)
        self.image.fill(color)
        
        self.mass = mass
        self.speed = speed
        self.vthreshold = vthreshold

        self.location = location
        self.velocity = [0.0, 0.0]
        self.last_location = location
        
        self.action = None
        self.animations = {}
        self.animation = None

    def set_animation(self, action: str, frames: list[pg.Surface], loop: bool=True, frame_duration: float=5.0, frame_offset: list[int]=[0, 0]) -> None:
        try:
            self.animations[action] = Animation(frames, loop, frame_duration, frame_offset)
            self.animation = self.animations[action]
            self.action = action
        except Exception as err: pass

    def rem_animation(self, action: str) -> None:
        try:
            del self.animations[action]
        except KeyError as err: return None

    def set_action(self, action: str) -> None:
        if self.action == action: return None
        try:
            self.action = action
            self.animation.reset()
            self.animation = self.animations.get(action, None)
        except KeyError as err: return None

    def get_rect(self) -> pg.Rect: return pg.Rect(self.location, self.size)

    def set_image(self, image: pg.Surface) -> None:
        if isinstance(image, pg.Surface):
            self.image = image
        elif image is None:
            self.image = pg.Surface(self.size)
            self.image.fill(self.color)

    def set_velocity(self, vx: float=0.0, vy: float=0.0) -> None:
        if vx: self.velocity[0] = vx
        if vy: self.velocity[1] = vy

    def get_facing(self) -> str:
        dx = None
        dy = None
        v = self.velocity
        if v[0] < 0:
            dx = "L"
        if v[0] > 0:
            dx = "R"
        if v[1] < 0:
            dy = "U"
        if v[1] > 0:
            dy = "D"

        if dx and dy: return dx+dy
        return dx if dy is None else dy

    def update(self, delta_time: float) -> None:
        # Apply movement
        self.last_location = self.location
        self.location[0] += self.velocity[0] * delta_time
        self.location[1] += self.velocity[1] * delta_time
        self.velocity = [*map(lambda v: damp_lin(v, self.mass, self.vthreshold, delta_time), self.velocity)]

        if self.animation:
            self.animation.update()
            self.image = self.animation.get_frame()
# ------------------------------------------------------------ #
