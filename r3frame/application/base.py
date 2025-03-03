from r3frame.globals import pg
from r3frame.utils import _asset_path
from r3frame.application.ui import Button
from r3frame.application.scene import Scene
from r3frame.application.events import Event_Manager
from r3frame.application.inputs import Keyboard, Mouse, Action_Map
from r3frame.application.resource import Clock, Window, Camera, Renderer, Asset_Manager

class Application:
    def __init__(self, name: str="My App", window_size: list[int]=[800, 600]) -> None:
        self.name = name
        self.clock = Clock()
        self.assets = Asset_Manager()
        self.events = Event_Manager()

        self.scene: str = None
        self.active_scene: Scene = None
        self.scenes: dict[str, Scene] = {}

        self.window = Window(window_size, window_size)
        self.window.title = name
        self.window.icon = pg.image.load(_asset_path("images/r3-logo.ico"))
        self.window.configure()

        self.camera = Camera(self.window)
        self.renderer = Renderer(self.camera)

    def set_scene(self, scene: Scene) -> None:
        self.scenes[scene.name] = scene
        self.scene = scene.name
        self.active_scene = self.scenes[self.scene]
    def rem_scene(self, key: str) -> Scene|None:
        if self.get_scene(key) is not None:
            del self.scenes[key]
            self.scene = None
            self.active_scene = None
    def get_scene(self, key: str) -> Scene|None: return self.scenes.get(key, None)

    def load_assets(self) -> None: raise NotImplementedError
    def load_scenes(self) -> None: raise NotImplementedError
    def load_objects(self) -> None: raise NotImplementedError

    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError

    def run(self) -> None:
        self.load_scenes()
        self.load_assets()
        self.load_objects()
        while not self.events.quit:
            self.clock.update()
            self.events.update()

            self.handle_events()

            self.handle_update()
            if self.active_scene:
                self.scenes[self.scene].handle_update(self.events)
                for interface in self.active_scene.interfaces:
                    self.active_scene.interfaces[interface].update(self.events)
            self.camera.update(self.clock.delta)

            self.handle_render()
            self.renderer.flush()
            if self.active_scene:
                self.scenes[self.scene].handle_render()
                for interface in self.active_scene.interfaces:
                    self.active_scene.interfaces[interface].render()

            self.window.update()
            self.clock.rest()
