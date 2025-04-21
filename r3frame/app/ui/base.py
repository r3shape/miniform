from r3frame.globs import pg
from r3frame.app.input import Mouse
from r3frame.app.resource import Window
from r3frame.util import point_inside
from r3frame.app.ui.element import Element

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

        self.elements: dict[str, Element] = {}
        
        self.font_path = font_path
        self.text_size: int = text_size
        self.text_fields: dict[str, str] = {}
        self.text_color: list[int] = text_color
        self.title_color: list[int] = title_color
        self.font: pg.Font = pg.Font(font_path, text_size)

        self.show_name = True
        self.display = pg.Surface(size)

    def set_element(self, key: str, element: Element) -> None:
        self.elements[key] = element
    
    def get_element(self, key: str) -> Element|None:
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> Element|None:
        if self.get_element(key) is not None:
            del self.elements[key]

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

        for element in self.elements.values():    # render elements
            element.render(self.window.window)

    def update(self, event_manager) -> None:
        for element in self.elements.values():
            mouse_location = Mouse.get_location()
            mouse_within = point_inside(mouse_location, [
                element.location[0] - element.border_size[0], element.location[1] - element.border_size[1],
                element.size[0] + element.border_size[0], element.size[1] + element.border_size[1]
            ])
            if not element.hovered and mouse_within:
                Mouse.Hovering = element
                element.hovered = True
                element.on_hover()
            if element.hovered and not mouse_within:
                Mouse.Hovering = None
                element.hovered = False
                element.on_unhover()
            if element.hovered and event_manager.mouse_pressed(Mouse.LeftClick):
                event_manager.mouse[Mouse.LeftClick] = 0    # shouldnt need this but fixes the element double-click issue :|
                element.on_click()
