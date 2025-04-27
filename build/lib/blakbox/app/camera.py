from blakbox.globs import pg
from blakbox.game.obj import Object
from blakbox.app.window import Window
from blakbox.util import damp_lin, add_v2, div_v2, scale_v2

# ------------------------------------------------------------ #
class Camera:
    class MODES:
        CENTER_ON: int = 1

    def __init__(self, window: Window):
        self.window = window
        self.mode = 0
        self.drag = 18
        self.speed = 50
        self.pos = [0, 0]
        self.velocity = [0.0, 0.0]
        self.last_location = self.pos

        self.bounds = window.display_size
        self.viewport_size = window.display_size
        self.viewport_scale = [
            self.window.screen_size[0] / self.viewport_size[0],
            self.window.screen_size[1] / self.viewport_size[1]
        ]
        self.mod_viewport(-self.viewport_size[0] - self.viewport_size[1])
        self.center = add_v2(self.pos, div_v2(self.viewport_size, 2))

    def configure(self, display_size: list[int]) -> None:
        self.bounds = display_size
        self.viewport_size = display_size
        self.viewport_scale = [
            self.window.screen_size[0] / self.viewport_size[0],
            self.window.screen_size[1] / self.viewport_size[1]
        ]
        self.center = self.center = add_v2(self.pos, div_v2(self.viewport_size, 2))
        self.mod_viewport(-self.viewport_size[0] - self.viewport_size[1])

    @property
    def offset(self) -> list[float]:
        return scale_v2(self.pos, -1.0)

    def get_center(self, size: list[int]) -> pg.Rect:
        return pg.Rect([self.center[0] - size[0] / 2, self.center[1] - size[1] / 2], size)

    def get_viewport(self) -> pg.Rect:
        return pg.Rect(self.pos, self.viewport_size)

    def set_velocity(self, vx: float=0.0, vy: float=0.0) -> None:
        if vx: self.velocity[0] = vx
        if vy: self.velocity[1] = vy

    def mod_viewport(self, delta: float) -> list[int]:
        delta *= (min(self.viewport_size) * 0.05)  # scale the delta by 5% of the viewport size
        aspect_ratio = self.viewport_size[0] / self.viewport_size[1]

        new_width = min(self.bounds[0], max(260, self.viewport_size[0] + delta))
        new_height = min(self.bounds[1], max(260, self.viewport_size[1] + delta))

        if new_width / new_height != aspect_ratio:
            if new_width == self.bounds[0]:
                new_height = new_width / aspect_ratio
            if new_height == self.bounds[1]:
                new_width = new_height * aspect_ratio

        self.viewport_size = [new_width, new_height]
        self.center = add_v2(self.pos, div_v2(self.viewport_size, 2))

        return self.viewport_size

    def center_on(self, size: list[int], pos: list[int|float]) -> None:
        if self.mode != self.MODES.CENTER_ON: self.mode = self.MODES.CENTER_ON
        target_center = [
            (pos[0] + self.viewport_size[0] / 2) + size[0] / 2,
            (pos[1] + self.viewport_size[1] / 2) + size[1] / 2
        ]

        dist = [
            (self.center[0] - target_center[0]) + self.viewport_size[0] / 2,
            (self.center[1] - target_center[1]) + self.viewport_size[1] / 2
        ]
    
        self.velocity = [
            (-dist[0] * self.speed) * (1 / self.drag),
            (-dist[1] * self.speed) * (1 / self.drag)
        ]

    def update(self, delta_time: float) -> None:
        self.viewport_scale = [
            self.window.screen_size[0] / self.viewport_size[0],
            self.window.screen_size[1] / self.viewport_size[1]
        ]
        self.last_location = self.pos
        self.velocity = [damp_lin(v, self.speed, 3, delta_time) for v in self.velocity]
        self.pos[0] = max(0, min(self.bounds[0] - self.viewport_size[0], self.pos[0] + self.velocity[0] * delta_time))
        self.pos[1] = max(0, min(self.bounds[1] - self.viewport_size[1], self.pos[1] + self.velocity[1] * delta_time))
        self.center = add_v2(self.pos, div_v2(self.viewport_size, 2))
# ------------------------------------------------------------ #