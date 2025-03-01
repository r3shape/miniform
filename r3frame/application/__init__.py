import r3frame.utils as utils
import r3frame.version as version
import r3frame.application.ui as ui
import r3frame.application.scene as scene
import r3frame.application.inputs as inputs
import r3frame.application.events as events
import r3frame.application.resource as resource

from r3frame.objects.world import Grid_Map, Quad_Map

class Application:
    def __init__(self, name: str="My App") -> None:
        self.name = name
        self.clock = resource.Clock()
        self.events = events.Event_Manager()

        self.scene: str = None
        self.active_scene: scene.Scene = None
        self.scenes: dict[str, scene.Scene] = {}

    def set_scene(self, scene: scene.Scene) -> None:
        self.scenes[scene.name] = scene
        self.scene = scene.name
        self.active_scene = self.scenes[self.scene]
    def rem_scene(self, key: str) -> scene.Scene|None:
        if self.get_scene(key) is not None:
            del self.scenes[key]
            self.scene = None
            self.active_scene = None
    def get_scene(self, key: str) -> scene.Scene|None: return self.scenes.get(key, None)

    def load_assets(self) -> None: raise NotImplementedError
    def load_objects(self) -> None: raise NotImplementedError

    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError

    def run(self) -> None:
        self.load_assets()
        self.load_objects()
        while not self.events.quit:
            self.clock.update()
            self.events.update()

            self.handle_events()
            if isinstance(inputs.Mouse.Hovering, ui.Button) and self.events.mouse_pressed(inputs.Mouse.LeftClick):
                inputs.Mouse.Hovering.on_click()

            self.handle_update()
            if self.scene is not None:
                self.scenes[self.scene].camera.update(self.clock.delta)
                self.scenes[self.scene].handle_update()

            self.handle_render()
            if self.scene is not None:
                self.scenes[self.scene].renderer.flush()
                self.scenes[self.scene].handle_render()
                self.scenes[self.scene].window.update()

            self.clock.rest()