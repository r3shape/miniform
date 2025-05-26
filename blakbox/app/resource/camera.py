from blakbox.globs import pg
from blakbox.app.resource.window import BOXwindow
from blakbox.app.resource.object import BOXobject, OBJECT_FLAG
from blakbox.util import add_v2, sub_v2, div_v2, scale_v2

# ------------------------------------------------------------ #
class BOXcamera(BOXobject):
    def __init__(self, window: BOXwindow) -> None:
        super().__init__(size=[1, 1], color=[0, 0, 0], bounds=window.display_size)
        self.drag: int = 10
        self.zoom: float = 1.0
        self.window: BOXwindow = window
        self.viewport_size: list[int] = window.display_size
        self.viewport_scale = [window.screen_size[0] / self.viewport_size[0],
                               window.screen_size[1] / self.viewport_size[1]]
        
        self.mod_viewport(-self.viewport_size[0] - self.viewport_size[1])
        self.set_state(OBJECT_FLAG.BOUNDED)

    @property
    def viewport(self) -> pg.Rect:
        return pg.Rect(self.pos, self.viewport_size)

    @property
    def offset(self) -> list[float]:
        return scale_v2(self.pos, -1.0)
    
    def center_rect(self, size: list[int]) -> pg.Rect:
        return pg.Rect(sub_v2(add_v2(self.pos, div_v2(self.viewport_size, 2)), div_v2(size, 2)), size)

    def mod_viewport(self, delta: float) -> list[int]:
        delta *= min(self.viewport_size) * 0.1  # scale the delta by 10% of the viewport size
        aspect_ratio = self.viewport_size[0] / self.viewport_size[1]

        new_width = min(self.bounds[0], max(260, self.viewport_size[0] + delta))
        new_height = min(self.bounds[1], max(260, self.viewport_size[1] + delta))

        if new_width / new_height != aspect_ratio:
            if new_width == self.bounds[0]:
                new_height = new_width / aspect_ratio
            if new_height == self.bounds[1]:
                new_width = new_height * aspect_ratio

        self.viewport_size = [new_width, new_height]

        return self.viewport_size

    def follow(self, object: BOXobject) -> None:
        dist = add_v2(sub_v2(self.center, object.center), div_v2(self.viewport_size, 2))
        self.vel = [(-dist[0] * object.speed / 4) * (1 / self.drag),
                    (-dist[1] * object.speed / 4) * (1 / self.drag)]

    def update(self, dt):
        self.viewport_scale = [self.window.screen_size[0] / self.viewport_size[0],
                               self.window.screen_size[1] / self.viewport_size[1]]
        self.pos[0] = max(0, min(self.bounds[0] - self.viewport_size[0], self.pos[0] + self.transform[0] * dt))
        self.pos[1] = max(0, min(self.bounds[1] - self.viewport_size[1], self.pos[1] + self.transform[1] * dt))
# ------------------------------------------------------------ #