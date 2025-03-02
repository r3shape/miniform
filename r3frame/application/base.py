from r3frame.application.ui import Button
from r3frame.application.scene import Scene
from r3frame.application.events import Event_Manager
from r3frame.application.inputs import Keyboard, Mouse, Action_Map
from r3frame.application.resource import Clock, Window, Camera, Renderer

class Application:
    def __init__(self, name: str="My App") -> None:
        self.name = name
        self.clock = Clock()
        self.events = Event_Manager()

        self.scene: str = None
        self.active_scene: Scene = None
        self.scenes: dict[str, Scene] = {}

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
            if self.scene is not None:
                self.scenes[self.scene].camera.update(self.clock.delta)
                self.scenes[self.scene].handle_update(self.events)

            self.handle_render()
            if self.scene is not None:
                self.scenes[self.scene].renderer.flush()
                self.scenes[self.scene].handle_render()
                self.scenes[self.scene].window.update()

            self.clock.rest()