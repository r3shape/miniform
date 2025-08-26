from miniform.imports import pg, random
import miniform

class MiniCameraProc(miniform.MiniAtom):
    def __init__(self, app) -> None:
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.window: miniform.resource.Hwindow = app.window

        self.deadzone: float = 4.0
        self.damp_value: float = 1.0
        self.damp_threshold: float = 8.0
        
        self.shake_timer: float = 0.0
        self.shake_intensity: float = 1.0
        self.shake_offset: list[float] = [0.0, 0.0]
        
        self.velocity: list[float] = [0.0, 0.0]

        self.viewport_pos: list[float] = [0.0, 0.0]
        self.viewport_size: list[int] = [app.window.size[0] // 2, app.window.size[1] // 2]
        self.viewport_scale: list[float] = [
            app.window.size[0] / self.viewport_size[0],
            app.window.size[1] / self.viewport_size[1]]
    
    @property
    def viewport_width(self) -> float:
        return self.viewport_size[0]
    @property
    def viewport_height(self) -> float:
        return self.viewport_size[1]
    @property
    def viewport_area(self) -> float:
        return self.viewport_size[0] * self.viewport_size[1]

    @property
    def viewport_x(self) -> float:
        return self.viewport_pos[0]
    @property
    def viewport_y(self) -> float:
        return self.viewport_pos[1]
    @property
    def viewport_center(self) -> list[float]:
        return miniform.utils.add_v2(self.viewport_pos, miniform.utils.div_v2(self.viewport_size, 2))
    
    def project(self, pos: list[float]) -> list[float]:
        if not isinstance(pos, list): return pos
        return miniform.utils.sub_v2(pos, miniform.utils.sub_v2(self.viewport_pos, self.shake_offset))

    def zoom(self, delta: float) -> None:
        # scale zoom delta by 10% vp size
        delta *= min(self.viewport_size) * 0.1

        self.viewport_size[1] = min(self.window.size[1] * 2, max(self.window.size[1] / 12, self.viewport_size[1] + delta))
        self.viewport_size[0] = self.viewport_size[1] * self.window.aspect

        self.viewport_scale: list[float] = [
            self.window.size[0] / self.viewport_size[0],
            self.window.size[1] / self.viewport_size[1]]

        self.set_flag(miniform.MiniCameraFlag.CAMERA_DIRTY)

    def shake(self, intensity: float, time: float = 0.5) -> None:
        if not isinstance(time, (int, float))\
        or not isinstance(intensity, (int, float)):
            return

        self.shake_intensity = intensity
        self.shake_timer = time

    def move_to(self, pos: list[float]) -> None:
        diff = miniform.utils.sub_v2(pos, self.viewport_center)
        dist = miniform.utils.mag_v2(diff)
        if int(dist) <= self.deadzone: return
        self.velocity[0] = diff[0]
        self.velocity[1] = diff[1]

    def set_velocity(self, vx: float=None, vy: float=None) -> None:
        if isinstance(vx, (int, float)): self.velocity[0] = vx
        if isinstance(vy, (int, float)): self.velocity[1] = vy

    def update(self, dt: float) -> None:
        self.viewport_pos[0] += self.velocity[0] * dt
        self.viewport_pos[1] += self.velocity[1] * dt

        self.velocity[0] *= (1 - self.damp_value * dt)
        self.velocity[1] *= (1 - self.damp_value * dt)

        if abs(self.velocity[0]) < self.damp_threshold: self.velocity[0] = 0.0
        if abs(self.velocity[1]) < self.damp_threshold: self.velocity[1] = 0.0

        if self.shake_timer > 0.0:
            self.shake_offset = [random.uniform(-1, 1) * self.shake_intensity,
                                 random.uniform(-1, 1) * self.shake_intensity]
            self.shake_timer -= dt
        else:
            self.shake_timer = 0.0
            self.shake_intensity = 0.0
            self.shake_offset = [0.0, 0.0]
