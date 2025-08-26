from miniform.imports import pg
import miniform

class MiniWorldProc(miniform.MiniAtom):
    def __init__(
            self,
            app) -> None:
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.window: miniform.app.MiniWindow = app.window

        self.camera_proc: miniform.process.MiniCameraProc = app.camera_proc
        self.render_proc: miniform.process.MiniRenderProc = app.render_proc
        
    def update(self, dt: float) -> None:
        if not isinstance(self.app.world, miniform.resource.world.MiniWorld): return
        self.app.world.update(dt)
        self.app.world.render()

        self.app.mouse.pos.view = miniform.utils.div2_v2i(self.app.mouse.pos.screen, self.camera_proc.viewport_scale)
        self.app.mouse.pos.world = miniform.utils.add_v2(self.app.mouse.pos.view, self.camera_proc.viewport_pos)
