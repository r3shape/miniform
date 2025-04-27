from blakbox.globs import pg
from blakbox.util import abs_path, add_v2, div_v2, scale_v2

from blakbox.atom import Atom
from blakbox.app.proc import Process
from blakbox.app.scene import Scene
from blakbox.app.clock import Clock
from blakbox.app.window import Window
from blakbox.app.camera import Camera
from blakbox.app.renderer import Renderer
from blakbox.app.event import EventManager
from blakbox.app.input import Keyboard, Mouse
from blakbox.game.resource.image import Image
from blakbox.game.resource.surfmap import SurfMap

# ------------------------------------------------------------ #
class Application:
    def __init__(self, name: str="My App", window_size: list[int]=[800, 600]) -> None:
        self.state: int = 0
        self.name:str = name
        self.clock: Clock = Clock()
        self.events: EventManager = EventManager()
        self.surfmap: SurfMap = SurfMap(window_size)

        self.scene: str = None
        self.scene: Scene = None
        self.scenes: dict[str, Scene] = {}

        self.window: Window = Window(window_size, window_size, [1, 1], [58, 94, 123])
        self.window.mod_title(name)
        self.window.mod_icon(pg.image.load(abs_path("assets/images/logo.ico")))

        self.camera: Camera = Camera(self.window)
        self.renderer: Renderer = Renderer(self.surfmap, self.camera)

        self.processes: list[Process] = [None for _ in range(100)]
        self.configure()
    
    def _bsort(self) -> None:
        for _ in range(len(self.processes) - 1, 0, -1):
            for __ in range(_):
                if not self.processes[__] or not self.processes[__+1]: continue
                if self.processes[__].id > self.processes[__+1].id:
                    t = self.processes[__]
                    self.processes[__] = self.processes[__+1]
                    self.processes[__+1] = t
        
    def add_proc(self, proc: Process) -> None:
        if not isinstance(proc, Process): return
        self.processes[proc.id] = proc

    def rem_proc(self, pid: int) -> None:
        try:
            self.processes.pop(pid)
        except IndexError: pass

    def set_scene(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene
        self.scene = self.scenes[scene.name]
    
    def rem_scene(self, key: str) -> Scene|None:
        if self.get_scene(key) is not None:
            self.scenes.pop(key, None)
            self.scene = None
    
    def get_scene(self, key: str) -> Scene|None:
        return self.scenes.get(key, None)

    def configure(self) -> None: raise NotImplementedError
    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError

    def exit(self) -> None: raise NotImplementedError
    def run(self) -> None:
        while not self.events.quit:
            self.clock.tick()
            self.events.update()

            if isinstance(self.scene, Scene):
                self.scene.handle_events()
                self.handle_events()

                self.scene.handle_update()
                self.scene.interface.update(self.events)
                self.handle_update()
                self.camera.update(self.clock.delta)

                self.scene.handle_render()
                self.handle_render()
                self.renderer.render()
                self.scene.interface.render()
                
                if isinstance(Mouse.cursor.image, Image):
                    self.window.window.blit(Mouse.cursor.image.data, Mouse.pos.screen)

                Mouse.pos.world = scale_v2(div_v2(Mouse.pos.view, self.scene.tilemap.tilesize), self.scene.tilemap.tilesize)
            else:
                self.handle_events()

                self.handle_update()
                self.camera.update(self.clock.delta)

                self.handle_render()
                self.renderer.render()
                if isinstance(Mouse.cursor.image, Image):
                    self.window.window.blit(Mouse.cursor.image.data, Mouse.pos.screen)

            Mouse.pos.rel = pg.mouse.get_rel()
            Mouse.pos.screen = pg.mouse.get_pos()
            Mouse.pos.view = add_v2([Mouse.pos.screen[0] // self.camera.viewport_scale[0],
                                     Mouse.pos.screen[1] // self.camera.viewport_scale[1]], self.camera.pos)
            self.window.update()
            self.clock.rest()
        else:
            self.exit()
# ------------------------------------------------------------ #
