from oldbox.atom import Atom
from oldbox.globs import os, pg
from oldbox.util import abs_path
from oldbox.app.input import Mouse
from oldbox.util import point_inside

class ELEMENT_STATE:
    FILL: int = (1 << 0)
    HOVERED: int = (1 << 1)
    SHOW_TEXT: int = (1 << 2)
    SHOW_BORDER: int = (1 << 3)

# ------------------------------------------------------------ #
class Element(Atom):
    def __init__(
            self, text: str="Element",
            size: list[int]=[64, 64], color: list[int]=[0, 0, 0],
            padding: list[int]=[0, 0], location: list[int]=[0, 0],
            text_size: int=18, text_location: list[int]=[0, 0],
            text_color: list[int]=[255, 255, 255],
            font_path: str=abs_path("assets/fonts/megamax.ttf")
        ) -> None:
        super().__init__(0, 0)
        
        self.size = size
        self.location = location
        
        self.image_offset = [0, 0]
        self.image = pg.Surface(size)
        self.color: list[int] = color

        self.elements: dict[str, Element] = {}
        self.padding: list[int] = padding

        self.border_size = [1, 1]
        self.border_offset = [0, 0]
        self.border_radius = [0, 0, 0, 0]
        self.border_color = [255, 255, 255]

        self.text = text
        self.text_size: int = text_size
        self.text_color: list[int] = text_color
        self.text_location: list[int] = text_location

        self.font_path = font_path
        self.font: pg.Font = pg.Font(font_path, self.text_size)

        self.set_state(ELEMENT_STATE.FILL|ELEMENT_STATE.SHOW_TEXT)
    
    def load_font(self, font_path: str) -> None:
        if not isinstance(font_path, str) or not os.path.exists(font_path): return
        del self.font
        self.font_path = font_path
        self.font: pg.Font = pg.Font(font_path, self.text_size)

    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass

    def set_element(self, key: str, element: "Element") -> None:
        element.location = [
            element.location[0] + self.location[0],
            element.location[1] + self.location[1]
        ]
        self.elements[key] = element
    
    def get_element(self, key: str) -> "Element":
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if self.get_element(key) is not None:
            del self.elements[key]

    def border(self) -> pg.Rect:
        return pg.Rect(
            [(self.location[0] + self.border_offset[0]) - self.border_size[0],
             (self.location[1] + self.border_offset[1]) - self.border_size[1],], 
            [self.size[0] + self.border_size[0],
             self.size[1] + self.border_size[1],]
        )

    def render(self, surface: pg.Surface) -> None: 
        if self.get_state(ELEMENT_STATE.FILL):
            self.image.fill(self.color)
        
        if self.get_state(ELEMENT_STATE.SHOW_TEXT):
            self.image.blit(
                self.font.render(self.text, True, self.text_color, self.color),
                [self.text_location[0] + self.padding[0], self.text_location[1] + self.padding[1]]
            )

        surface.blit(self.image, [
            self.location[0] + self.image_offset[0],
            self.location[1] + self.image_offset[1]
        ])
        
        for element in self.elements.values():    # render elements
            element.render(surface)
        
        if self.get_state(ELEMENT_STATE.SHOW_BORDER):
            pg.draw.rect(
            surface=surface, color=self.border_color,
            rect=self.border(), width=self.border_size[0],
            border_top_left_radius=self.border_radius[0],
            border_top_right_radius=self.border_radius[1],
            border_bottom_left_radius=self.border_radius[2],
            border_bottom_right_radius=self.border_radius[3]
        )
            
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
