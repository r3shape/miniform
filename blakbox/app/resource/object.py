from blakbox.atom import BOXatom
from blakbox.globs import pg, math
from blakbox.util import add_v2, sub_v2, div_v2, mul_v2, damp_lin, norm_v2

class OBJECT_FLAG:
    BOUNDED: int = (1 << 0)
    VISIBLE: int = (1 << 1)

# ------------------------------------------------------------ #
class BOXobject(BOXatom):
    def __init__(
            self,
            tag: str = "BOXobject",
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            bounds: list[int] = [0, 0],
            color: list[int] = [0, 0, 0],
            ):
        super().__init__(0, 0)
        self.tag: str = tag
        self.atlas_id: int = None
        self.atlas_tag: str = None

        self.size: list[int] = size[:]
        self.color: list[int] = color[:]
        self.surface: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        self.surface.fill(color)
        
        self.speed: float = 100.0
        self.rotation: float = 0.0
        self.pos: list[float] = pos[:]
        self.vel: list[float] = [0.0, 0.0]
        self.bounds: list[int] = bounds[:]
        self.mvmt: list[float] = [0, 0, 0, 0]
        self.collisions: list[bool] = [0, 0, 0, 0]

        self.target_gap: float = 2.0
        self.target_pos: list[float] = None
        
        self.grid_cell: list[int] = [0, 0]  # cell occupied in BOXobjectgrid
        self._last_cell: list[int] = [0, 0] # last cell occupied in BOXobjectgrid

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    @property
    def center(self) -> list[float]:
        return add_v2(self.pos, div_v2(self.size, 2))

    @property
    def direction(self) -> list[float]:
        return [(self.mvmt[3] - self.mvmt[2]), (self.mvmt[1] - self.mvmt[0])]
    
    @property
    def transform(self) -> list[float]:
        return add_v2(mul_v2([(self.mvmt[3] - self.mvmt[2]), (self.mvmt[1] - self.mvmt[0])], [self.speed, self.speed]), self.vel)

    @property
    def rotated(self) -> tuple[pg.Surface, pg.Rect]:
        rot_surf = pg.transform.rotate(self.surface, self.rotation)
        rot_rect = rot_surf.get_rect(center=self.center)
        return rot_surf, rot_rect

    def set_color(self, color: list[int], fill: bool = False) -> None:
        self.color = color
        if fill: self.surface.fill(color)

    def set_colorkey(self, key: list[int]) -> None:
        self.surface.set_colorkey(key)

    def set_vel(self, vx: float=None, vy: float = None) -> None:
        if vx is not None: self.vel[0] = vx
        if vy is not None: self.vel[1] = vy

    def move_to(self, target: list[float]) -> None:
        self.target_pos = target[:]

    def look_to(self, target: list[float]) -> None:
        d = norm_v2(sub_v2(target, self.pos))
        self.rotation = math.degrees(math.atan2(-d[1], d[0]))

    def move(self, left: bool=None, right: bool=None, up: bool=None, down: bool=None) -> None:
        self.mvmt[0] = up if up is not None else self.mvmt[0]
        self.mvmt[1] = down if down is not None else self.mvmt[1]
        self.mvmt[2] = left if left is not None else self.mvmt[2]
        self.mvmt[3] = right if right is not None else self.mvmt[3]
    
    def on_collide(self, object: "BOXobject") -> None: pass
    def on_collide_up(self, object: "BOXobject") -> None: pass
    def on_collide_down(self, object: "BOXobject") -> None: pass
    def on_collide_left(self, object: "BOXobject") -> None: pass
    def on_collide_right(self, object: "BOXobject") -> None: pass

    def _aabbx(self, transform: list[float], collidables: list["BOXobject"]) -> None:
        rect = self.rect
        for obj in collidables:
            if not obj: continue
            if obj == self: continue
            if rect.colliderect(obj.rect):
                if transform[0] < 0:
                    rect.left = obj.rect.right
                    self.mvmt[2] = 0
                    self.collisions[2] = 1
                    self.on_collide(obj)
                    self.on_collide_left(obj)
                if transform[0] > 0:
                    rect.right = obj.rect.left
                    self.mvmt[3] = 0
                    self.collisions[3] = 1
                    self.on_collide(obj)
                    self.on_collide_right(obj)
                self.pos[0] = rect.x
    
    def _aabby(self, transform: list[float], collidables: list["BOXobject"]) -> None:
        rect = self.rect
        for obj in collidables:
            if not obj: continue
            if obj == self: continue
            if rect.colliderect(obj.rect):
                if transform[1] < 0:
                    rect.top = obj.rect.bottom
                    self.mvmt[0] = 0
                    self.collisions[0] = 1
                    self.on_collide(obj)
                    self.on_collide_up(obj)
                if transform[1] > 0:
                    rect.bottom = obj.rect.top
                    self.mvmt[1] = 0
                    self.collisions[1] = 1
                    self.on_collide(obj)
                    self.on_collide_down(obj)
                self.pos[1] = rect.y

    def update(self, dt: float, collidables: list["BOXobject"]=[]) -> None:
        if self.target_pos:
            dx = self.target_pos[0] - self.center[0]
            dy = self.target_pos[1] - self.center[1]
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < self.target_gap:
                self.target_pos = None
                self.mvmt = [0, 0, 0, 0]
            else:
                dir_x = dx / dist
                dir_y = dy / dist
                self.vel[0] = dir_x * self.speed
                self.vel[1] = dir_y * self.speed

        transform = self.transform
        if self.get_state(OBJECT_FLAG.BOUNDED):
            self.pos[0] = max(0, min(self.bounds[0] - self.size[0], self.pos[0] + transform[0] * dt))
            self._aabbx(transform, collidables)
            self.pos[1] = max(0, min(self.bounds[1] - self.size[1], self.pos[1] + transform[1] * dt))
            self._aabby(transform, collidables)
        else:
            self.pos[0] += transform[0] * dt
            self._aabbx(transform, collidables)
            self.pos[1] += transform[1] * dt
            self._aabby(transform, collidables)

        self.vel[0] = damp_lin(self.vel[0], self.speed * 4, 5, dt)
        self.vel[1] = damp_lin(self.vel[1], self.speed * 4, 5, dt)
# # ------------------------------------------------------------ #