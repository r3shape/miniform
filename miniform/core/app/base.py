from miniform.imports import pg, os, json
import miniform

class MiniApp(miniform.MiniAtom):
    def __init__(
            self,
            title: str="Miniform App",
            clock_rate: float = 0.5,
            clock_target: float = 60.0,
            window_size: list[int] = [1280, 720],
            window_color: list[int] = [55, 55, 55]) -> None:
        super().__init__()
        self.configure(title, clock_rate, clock_target, window_size, window_color)

    def configure(
            self,
            title: str="Miniform App",
            clock_rate: float = 0.5,
            clock_target: float = 60.0,
            window_size: list[int] = [1280, 720],
            window_color: list[int] = [55, 55, 55]) -> None:
        self.title: str = str(title)

        self.events: miniform.app.MiniEvents = miniform.app.MiniEvents(self)
        self.clock: miniform.app.MiniClock = miniform.app.MiniClock(clock_rate, clock_target)
        self.window: miniform.app.MiniWindow = miniform.app.MiniWindow(title, window_size, window_color)
        
        self.mouse: miniform.app.inputs.Hmouse = miniform.app.MiniMouse
        self.keyboard: miniform.app.inputs.Hkeyboard = miniform.app.MiniKeyboard

        self.camera_proc: miniform.process.MiniCameraProc = miniform.process.MiniCameraProc(self)
        self.render_proc: miniform.process.MiniRenderProc = miniform.process.MiniRenderProc(self)
        self.world_proc: miniform.process.MiniWorldProc = miniform.process.MiniWorldProc(self)
        self.interface_proc: miniform.process.MiniInterfaceProc = miniform.process.MiniInterfaceProc(self.window)
        
        self.cache: miniform.resource.MiniCache = miniform.resource.MiniCache(self)
        self.world: miniform.resource.world.MiniWorld = None

        self._freeze()

        self.set_flag(miniform.MiniAppFlag.APP_RUNNING)
        self.set_flag(miniform.MiniAppFlag.APP_DRAW_INTERFACE)

    def init(self) -> None: raise NotImplementedError
    def exit(self) -> None: raise NotImplementedError

    def set_world(self, world: "miniform.resource.world.MiniWorld") -> None:
        if not callable(world) or not isinstance(world, type): return
        self.world = world(self)

        self.world._unfreeze()
        self.world.init()
        self.world._freeze()

    def rem_world(self) -> None:
        if not isinstance(self.world, miniform.resource.world.MiniWorld): return
        self.world._unfreeze()
        self.world.exit()
        self.world._freeze()
        self.world = None

    def update_hook(self, dt:float) -> None: pass
    def render_hook(self) -> None: pass

    def run(self) -> None:
        self.init()
        while self.get_flag(miniform.MiniAppFlag.APP_RUNNING):
            self.events.update()
            self.window.clear()
            
            self.mouse.pos.screen = pg.mouse.get_pos()
            self.mouse.pos.rel = pg.mouse.get_rel()

            self.update_hook(self.clock.delta)

            # pipeline updates
            self.world_proc.update(self.clock.delta)    # separate thread for physics
            self.camera_proc.update(self.clock.delta)
            self.render_proc.update()
            self.interface_proc.update(self.mouse, self.events)
            
            self.render_hook()

            self.window.update()
            self.clock.update()
        else:
            self.exit()
            self.cache.clear()
