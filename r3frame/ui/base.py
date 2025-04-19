from r3frame.globs import pg
from r3frame.input import Mouse
from r3frame.rsrc import Window
from r3frame.util import point_inside
from r3frame.ui.button import Button
from r3frame.ui.tooltip import Tooltip

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

        self.buttons: dict[str, Button] = {}
        self.tooltips: dict[str, Button] = {}
        
        self.font_path = font_path
        self.text_size: int = text_size
        self.text_fields: dict[str, str] = {}
        self.text_color: list[int] = text_color
        self.title_color: list[int] = title_color
        self.font: pg.Font = pg.Font(font_path, text_size)

        self.show_name = True
        self.display = pg.Surface(size)

    def set_button(self, key: str, button: Button) -> None:
        self.buttons[key] = button
    
    def get_button(self, key: str) -> Button|None:
        return self.buttons.get(key, None)
    
    def rem_button(self, key: str) -> Button|None:
        if self.get_button(key) is not None:
            del self.buttons[key]

    def set_tooltip(self, key: str, tooltip:Tooltip) -> None:
        self.tooltips[key] = tooltip
    
    def get_tooltip(self, key: str) -> Tooltip|None:
        return self.tooltips.get(key, None)
    
    def rem_tooltip(self, key: str) -> Tooltip|None:
        if self.get_tooltip(key) is not None:
            del self.tooltips[key]

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
        if self.show_name: self.window.window.blit(self.font.render(self.name, True, self.title_color), self.location)
       
        for index, field in enumerate(self.text_fields.keys()): # render text fields
            text = f"{field}: {self.text_fields[field]["text"]}"
            color = self.text_fields[field]["color"]
            text_surface = self.font.render(text, True, self.text_color if not color else color)
            text_location = [
                self.location[0],
                self.location[1] + (text_surface.get_size()[1] * (index + 1))
            ]
            self.window.window.blit(text_surface, text_location)

        for tooltip in self.tooltips.values():  # render tooltips
            tooltip.render(self.window.window)
        for button in self.buttons.values():    # render buttons
            button.render(self.window.window)

    def update(self, event_manager) -> None:
        for button in self.buttons.values():
            mouse_location = Mouse.get_location()
            mouse_within = point_inside(mouse_location, [
                button.location[0] - button.border_size[0], button.location[1] - button.border_size[1],
                button.size[0] + button.border_size[0], button.size[1] + button.border_size[1]
            ])
            if not button.hovered and mouse_within:
                Mouse.Hovering = button
                button.hovered = True
                button.on_hover()
            if button.hovered and not mouse_within:
                Mouse.Hovering = None
                button.hovered = False
                button.on_unhover()
            if button.hovered and event_manager.mouse_pressed(Mouse.LeftClick):
                event_manager.mouse[Mouse.LeftClick] = 0    # shouldnt need this but fixes the button double-click issue :|
                button.on_click()
