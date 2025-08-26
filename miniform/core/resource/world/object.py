from miniform.imports import pg
import miniform

class MiniStaticObject(miniform.MiniAtom):
    def __init__(
            self,
            pos: list[float],
            size: list[int]=[32, 32],
            color: list[int]=[172, 50, 50], tag: str=None) -> None:
        super().__init__()
        self.tag: str = tag
        self.spatial_index: set[tuple[int]] = set()

        self.size: list[int] = [*map(int, size)]
        self.half_size: list[int] = [self.size[0] // 2, self.size[1] // 2]

        self.color: list[int] = [*map(int, color)]
        self.pos: list[float] = [*map(float, pos)]
        
        self.surface: pg.Surface = pg.Surface(self.size, pg.SRCALPHA)
        self.surface.fill(self.color)

        self.set_flag(miniform.MiniObjectFlag.OBJECT_STATIC)
        self.set_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS)
        self._freeze()

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    @property
    def frect(self) -> pg.Rect:
        return pg.FRect(self.pos, self.size)

    @property
    def center(self) -> list[float]:
        return miniform.utils.add_v2(self.pos, miniform.utils.div_v2(self.size, 2))
    
    def render_hook(self) -> None: pass

class MiniDynamicObject(MiniStaticObject):
    def __init__(
            self,
            pos: list[float],
            size: list[int]=[32, 32],
            
            mass: float=25.0,

            color: list[int]=[95, 205, 228],
            tag: str = None) -> None:
        super().__init__(pos, size, color, tag)
        
        self.mass: float = float(mass)
        self.velocity: list[float] = [0.0, 0.0]
        
        self.swap_flag(miniform.MiniObjectFlag.OBJECT_STATIC, miniform.MiniObjectFlag.OBJECT_DYNAMIC)
        self.set_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS)

    def set_velocity(self, vx: float=None, vy: float=None) -> None:
        if isinstance(vx, (int, float)): self.velocity[0] = vx
        if isinstance(vy, (int, float)): self.velocity[1] = vy

    def update_hook(self, dt: float) -> None: pass
    def collision_hook(self, dt: float) -> None: pass

    def aabbx(self, neighbors, dt: float) -> None:
        if self.get_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS) == False: return
        rect = self.rect
        for obj in neighbors:
            if obj == self: continue
            if obj.get_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS) == False: continue
            rect2 = obj.rect
            if rect.colliderect(rect2):
                if self.velocity[0] < 0.0:
                    rect.left = rect2.right
                    self.pos[0] = rect.x + (rect2.right - rect.left)
                elif self.velocity[0] > 0.0:
                    rect.right = rect2.left
                    self.pos[0] = rect.x + (rect2.left - rect.right)
                self.velocity[0] = 0.0
                self.collision_hook(dt)

    def aabby(self, neighbors, dt: float) -> None:
        if self.get_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS) == False: return

        rect = self.rect
        for obj in neighbors:
            if obj == self: continue
            if obj.get_flag(miniform.MiniObjectFlag.OBJECT_COLLISIONS) == False: continue
            rect2 = obj.rect
            if rect.colliderect(rect2):
                if self.velocity[1] < 0.0:
                    rect.top = rect2.bottom
                    self.pos[1] = rect.y + (rect2.bottom - rect.top)
                elif self.velocity[1] > 0.0:
                    rect.bottom = rect2.top
                    self.pos[1] = rect.y + (rect2.top - rect.bottom)
                self.velocity[1] = 0.0
                self.collision_hook(dt)

    def update(self, neighbors, dt: float) -> None:
        self.pos[0] += self.velocity[0] * dt
        self.aabbx(neighbors, dt)
        self.pos[1] += self.velocity[1] * dt
        self.aabby(neighbors, dt)
        
        self.velocity = miniform.utils.scale_v2(self.velocity, (1 - (self.mass / 100.0) * dt))
        if abs(self.velocity[0]) < 0.8: self.velocity[0] = 0.0
        if abs(self.velocity[1]) < 0.8: self.velocity[1] = 0.0
