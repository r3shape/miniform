from r3frame.globals import pg
from r3frame.application.inputs import Mouse
from r3frame.application.resource import Window
from r3frame.application.ui.button import Button

class Interface:
    def __init__(
            self, name: str, window: Window,
            size: list[int], location: list[float],
            font_path:str, title_color:list[int]=[255, 255, 255],
            text_color:list[int]=[255, 255, 255], text_size: int=18
        ) -> None:
        pg.font.init()
        self.name = name
        self.window = window
        self.size: list[int] = size
        self.location: list[float] = location

        self.buttons = {}
        
        self.font_path = font_path
        self.text_size: int = text_size
        self.text_fields: dict[str, str] = {}
        self.text_color: list[int] = text_color
        self.title_color: list[int] = title_color
        self.font: pg.Font = pg.Font(font_path, text_size)

    def set_button(
            self, key: str, text: str="Button",
            size: list[int]=[64, 64], location: list[int|float]=[0, 0], title_color:list[int]=[255, 255, 255],
            color: list[int]=[0, 0, 0], text_color:list[int]=[255, 255, 255], text_size: int=18, padding: list[int]=[0, 0],
            border_size: list[int]=[5, 5], border_radius: list[int]=[0, 0, 0, 0], border_color: list[int]=[255, 255, 255],
        ) -> None:
        self.buttons[key] = Button(
            self.font_path, text, size, location,
            color, text_color, text_size, padding,
            border_size, border_radius, border_color
        )
    
    def get_button(self, key: str) -> Button|None:
        return self.buttons.get(key, None)
    
    def rem_button(self, key: str) -> Button|None:
        if self.get_button(key) is not None:
            del self.buttons[key]

    def set_text_field(self, field: str, text: str, color: list[int]=None) -> bool:
        try:
            self.text_fields[field] = {"text": text, "color": color}
            return True
        except KeyError as e:
            return False
    
    def rem_text_field(self, field: str) -> bool:
        try:
            del self.text_fields[field]
            return True
        except KeyError as e:
            return False

    def render(self) -> None:
        for button in self.buttons.values():
            button.render(self.window.window)
        self.window.window.blit(self.font.render(self.name, True, self.title_color), self.location)
        for index, field in enumerate(self.text_fields.keys()):
            text = f"{field}: {self.text_fields[field]["text"]}"
            color = self.text_fields[field]["color"]
            text_surface = self.font.render(text, True, self.text_color if not color else color)
            text_location = [
                self.location[0],
                self.location[1] + (text_surface.get_size()[1] * (index + 1))
            ]
            self.window.window.blit(text_surface, text_location)

    def update(self, event_manager) -> None:
        if isinstance(Mouse.Hovering, Button) and event_manager.mouse_pressed(Mouse.LeftClick):
                Mouse.Hovering.on_click()
        for button in self.buttons.values():
            mouse_location = Mouse.get_location()
            if Mouse.Hovering == button and \
                   mouse_location[0] < button.location[0] or mouse_location[0] > button.location[0] + button.size[0]\
                or mouse_location[1] < button.location[1] or mouse_location[1] > button.location[1] + button.size[1]:
                    Mouse.Hovering = None
                    button.on_unhover()
            elif Mouse.Hovering != button and\
                mouse_location[0] >= button.location[0] and mouse_location[0] <= button.location[0] + button.size[0]\
            and mouse_location[1] >= button.location[1] and mouse_location[1] <= button.location[1] + button.size[1]:
                Mouse.Hovering = button
                button.on_hover()
