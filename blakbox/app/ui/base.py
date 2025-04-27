from blakbox.atom import Atom
from blakbox.globs import os, pg
from blakbox.app.input import Mouse
from blakbox.app.window import Window
from blakbox.util import point_inside
from blakbox.app.ui.element import ELEMENT_STATE, Element

# ------------------------------------------------------------ #
class Interface(Atom):
    def __init__(
            self, name: str, window: Window,
            size: list[int], location: list[float],
            font_path:str, title_color:list[int]=[255, 255, 255],
            text_color:list[int]=[255, 255, 255], text_size: int=18
        ) -> None:
        super().__init__(0, 0)
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

    def load_font(self, font_path: str) -> None:
        if not isinstance(font_path, str) or not os.path.exists(font_path): return
        del self.font
        self.font_path = font_path
        self.font: pg.Font = pg.Font(font_path, self.text_size)

    def set_element(self, key: str, element: Element) -> None:
        self.elements[key] = element
    
    def get_element(self, key: str) -> Element:
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
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
        if self.show_name: self.window.screen.blit(self.font.render(self.name, True, self.title_color), self.location)
       
        for index, field in enumerate(self.text_fields.keys()): # render text fields
            text = f"{field}: {self.text_fields[field]["text"]}"
            color = self.text_fields[field]["color"]
            text_surface = self.font.render(text, True, self.text_color if not color else color)
            text_location = [
                self.location[0],
                self.location[1] + (text_surface.get_size()[1] * (index + 1))
            ]
            self.window.screen.blit(text_surface, text_location)

        for element in self.elements.values():    # render elements
            element.render(self.window.screen)

    def update(self, event_manager) -> None:
        for element in self.elements.values():
            element.update(event_manager)
            mouse_within = point_inside(Mouse.pos.screen, [
                element.location[0] - element.border_size[0], element.location[1] - element.border_size[1],
                element.size[0] + element.border_size[0], element.size[1] + element.border_size[1]
            ])
            if not element.get_state(ELEMENT_STATE.HOVERED) and mouse_within:
                Mouse.Hovering = Element
                element.set_state(ELEMENT_STATE.HOVERED)
                element.on_hover()
            if element.get_state(ELEMENT_STATE.HOVERED) and not mouse_within:
                Mouse.Hovering = None
                element.rem_state(ELEMENT_STATE.HOVERED)
                element.on_unhover()
            if element.get_state(ELEMENT_STATE.HOVERED) and event_manager.mouse_pressed(Mouse.LeftClick):
                event_manager.mouse[Mouse.LeftClick] = 0    # shouldnt need this but fixes the element double-click issue :|
                element.on_click()
# ------------------------------------------------------------ #
