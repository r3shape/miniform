from r3frame.globs import pg
from r3frame.util import _asset_path

from r3frame.app.scene import Scene
from r3frame.app.event import EventManager
from r3frame.app.resource import Clock, Window, Camera, Renderer, AssetManager

class Application:
    def __init__(self, name: str="My App", window_size: list[int]=[800, 600]) -> None:
        self.name = name
        self.clock = Clock()
        self.assets = AssetManager()
        self.events = EventManager()

        self.scene: str = None
        self.scene: Scene = None
        self.scenes: dict[str, Scene] = {}

        self.window = Window(window_size, window_size)
        self.window.title = name
        self.window.icon = pg.image.load(_asset_path("images/r3-logo.ico"))
        self.window.configure(window_size)

        self.camera = Camera(self.window)
        self.renderer = Renderer(self.camera)

        self.configure()
    
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
            else:
                self.handle_events()

                self.handle_update()
                self.camera.update(self.clock.delta)

                self.handle_render()
                self.renderer.render()

            self.window.update()
            self.clock.rest()
        else:
            self.exit()
