import r3frame.utils as utils
import r3frame.version as version
import r3frame.application.ui as ui
import r3frame.application.inputs as inputs
import r3frame.application.events as events
import r3frame.application.resource as resource
import r3frame.application.resource as resource

from r3frame.objects.world import Grid_Map, Quad_Map

class Application:
    def __init__(self, name: str="My App", title: str="My Game", partition: str="GRID") -> None:
        self.clock = resource.Clock()
        self.events = events.Event_Manager()
        self.assets = resource.Asset_Manager()

        match partition.upper():
            case "GRID": self.partition = Grid_Map(1500, 1500, 8)
            case "QUAD": self.partition = Quad_Map(1500, 1500, 8)

        self.buttons = {}
        self.window = resource.Window([800, 600], self.partition.size)
    
        self.camera = resource.Camera(self.window)
        self.renderer = resource.Renderer(self.camera)

        self.dev = resource.DevDisplay(
            f"r3frame {version.R3FRAME_YEAR}.{version.R3FRAME_MINOR}.{version.R3FRAME_PATCH}",
            self.window, [100, 100], [0, 0], utils._asset_path("fonts/megamax.ttf"), text_size=20)

    def add_button(
            self, key: str, font_path:str, text: str="Button",
            size: list[int]=[64, 64], location: list[int|float]=[0, 0],
            color: list[int]=[0, 0, 0], text_color:list[int]=[255, 255, 255], text_size: int=18, padding: list[int]=[0, 0],
            border_size: list[int]=[5, 5], border_radius: list[int]=[0, 0, 0, 0], border_color: list[int]=[255, 255, 255],
        ) -> None:
        self.buttons[key] = ui.Button(
            font_path, text, size, location,
            color, text_color, text_size, padding,
            border_size, border_radius, border_color
        )
    
    def get_button(self, key: str) -> ui.Button|None:
        return self.buttons.get(key, None)

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

            self.camera.update(self.clock.delta)
            
            self.handle_update()

            self.handle_render()
            self.renderer.flush()
            self.dev.render()

            for button in self.buttons.values():
                button.render(self.window.window)
                mouse_location = inputs.Mouse.get_location()
                if inputs.Mouse.Hovering == button:
                    if mouse_location[0] < button.location[0] or mouse_location[0] > button.location[0] + button.size[0]\
                    or mouse_location[1] < button.location[1] or mouse_location[1] > button.location[1] + button.size[1]:
                        inputs.Mouse.Hovering = None
                        button.on_unhover()
                elif inputs.Mouse.Hovering != button and\
                    mouse_location[0] >= button.location[0] and mouse_location[0] <= button.location[0] + button.size[0]\
                and mouse_location[1] >= button.location[1] and mouse_location[1] <= button.location[1] + button.size[1]:
                    inputs.Mouse.Hovering = button
                    button.on_hover()

            self.window.update()
            self.clock.rest()