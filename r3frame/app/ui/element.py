from r3frame.globs import os, pg
from r3frame.util import abs_path
from r3frame.app.input import Mouse
from r3frame.util import point_inside

# ------------------------------------------------------------ #
class Element:
    def __init__(
            self, text: str="Element",
            size: list[int]=[64, 64], color: list[int]=[0, 0, 0],
            padding: list[int]=[0, 0], location: list[int]=[0, 0],
            text_size: int=18, text_location: list[int]=[0, 0],
            text_color: list[int]=[255, 255, 255],
            font_path: str=abs_path("assets/fonts/megamax.ttf")
        ) -> None:
        self.hovered = False
        self.show_text = True
        self.show_border = False

        self.size = size
        self.location = location
        self.image = pg.Surface(size)

        self.elements: dict[str, Element] = {}
        
        self.offset = [0, 0]
        self.color: list[int] = color
        self.padding: list[int] = padding

        self.border_size = [1, 1]
        self.border_radius = [0, 0, 0, 0]
        self.border_color = [255, 255, 255]

        self.text = text
        self.text_size: int = text_size
        self.text_color: list[int] = text_color
        self.text_location: list[int] = text_location

        self.font_path = font_path
        self.font: pg.Font = pg.Font(font_path, self.text_size)
    
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
            [(self.location[0] + self.offset[0]) - self.border_size[0],
             (self.location[1] + self.offset[1]) - self.border_size[1],], 
            [self.size[0] + self.border_size[0],
             self.size[1] + self.border_size[1],]
        )

    def render(self, surface: pg.Surface) -> None: 
        self.image.fill(self.color)
        
        if self.show_text:
            self.image.blit(
                self.font.render(self.text, True, self.text_color, self.color),
                [self.text_location[0] + self.padding[0], self.text_location[1] + self.padding[1]]
            )

        surface.blit(self.image, [
            self.location[0] + self.offset[0],
            self.location[1] + self.offset[1]
        ])
        
        for element in self.elements.values():    # render elements
            element.render(surface)
        
        if self.show_border:
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
            mouse_within = point_inside(Mouse.location.screen, [
                element.location[0] - element.border_size[0], element.location[1] - element.border_size[1],
                element.size[0] + element.border_size[0], element.size[1] + element.border_size[1]
            ])
            if not element.hovered and mouse_within:
                Mouse.Hovering = Element
                element.hovered = True
                element.on_hover()
            if element.hovered and not mouse_within:
                Mouse.Hovering = None
                element.hovered = False
                element.on_unhover()
            if element.hovered and event_manager.mouse_pressed(Mouse.LeftClick):
                event_manager.mouse[Mouse.LeftClick] = 0    # shouldnt need this but fixes the element double-click issue :|
                element.on_click()
# ------------------------------------------------------------ #
