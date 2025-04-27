from r3frame.globs import pg
from r3frame.util import abs_path

from r3frame.atom import Atom
from r3frame.app.proc import Process
from r3frame.app.scene import Scene
from r3frame.app.clock import Clock
from r3frame.app.window import Window
from r3frame.app.camera import Camera
from r3frame.app.renderer import Renderer
from r3frame.app.event import EventManager
from r3frame.app.input import Keyboard, Mouse
from r3frame.app.resource.image import Image
from r3frame.app.resource.manager import ResourceManager

# ------------------------------------------------------------ #
class Application:
    def __init__(self, name: str="My App", window_size: list[int]=[800, 600]) -> None:
        self.state: int = 0
        self.name:str = name
        self.clock: Clock = Clock()
        self.events: EventManager = EventManager()
        self.resource: ResourceManager = ResourceManager()

        self.scene: str = None
        self.scene: Scene = None
        self.scenes: dict[str, Scene] = {}

        self.window: Window = Window(window_size, window_size)
        self.window.title = name
        self.window.icon = pg.image.load(abs_path("assets/images/r3-logo.ico"))
        self.window.configure(window_size)

        self.camera: Camera = Camera(self.window)
        self.renderer: Renderer = Renderer(self.camera)

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
        self.window.configure(self.scene.display_size)
        self.camera.configure(self.scene.display_size)
    
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
            self.clock.update()
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
                    self.window.window.blit(Mouse.cursor.image.data, Mouse.location.screen)

                Mouse.location.world = [
                    Mouse.location.view[0] // self.scene.tilemap.tilesize,
                    Mouse.location.view[1] // self.scene.tilemap.tilesize
                ]
            else:
                self.handle_events()

                self.handle_update()
                self.camera.update(self.clock.delta)

                self.handle_render()
                self.renderer.render()
                if isinstance(Mouse.cursor.image, Image):
                    self.window.window.blit(Mouse.cursor.image.data, Mouse.location.screen)

            Mouse.location.rel = [*pg.mouse.get_rel()]
            Mouse.location.screen = [*pg.mouse.get_pos()]
            Mouse.location.view = [
                int(Mouse.location.screen[0] // self.camera.viewport_scale[0] + self.camera.location[0]),
                int(Mouse.location.screen[1] // self.camera.viewport_scale[1] + self.camera.location[1]),
            ]
            self.window.update()
            self.clock.rest()
        else:
            self.exit()
# ------------------------------------------------------------ #
