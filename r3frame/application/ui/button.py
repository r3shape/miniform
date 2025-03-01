from r3frame.globals import pg

class Button:
    def __init__(
            self, font_path:str, text: str="Button",
            size: list[int]=[64, 64], location: list[int|float]=[0, 0],
            color: list[int]=[0, 0, 0], text_color:list[int]=[255, 255, 255], text_size: int=18, padding: list[int]=[0, 0],
            border_size: list[int]=[5, 5], border_radius: list[int]=[0, 0, 0, 0], border_color: list[int]=[255, 255, 255],
        ) -> None:
        self.image = pg.Surface(size)

        self.size = size
        self.color = color
        self.location = location

        self.border_size = border_size
        self.border_radius = border_radius
        self.border_color = border_color
        
        self.text = text
        self.padding = padding
        self.font_path = font_path
        self.text_size: int = text_size
        self.text_color: list[int] = text_color
        self.font: pg.Font = pg.Font(font_path, self.text_size)

    def border(self) -> pg.Rect:
        return pg.Rect(
            [self.location[0] - self.border_size[0],
             self.location[1] - self.border_size[1],], 
            [self.size[0] + self.border_size[0],
             self.size[1] + self.border_size[1],]
        )
    
    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass

    def render(self, surface: pg.Surface) -> None:
        self.image.fill(self.color)
        self.image.blit(
        self.font.render(self.text, True, self.text_color, self.color), [self.padding[0], self.padding[1]])
        surface.blit(self.image, self.location)
        pg.draw.rect(surface, self.border_color, self.border(), width=self.border_size[0],
            border_top_left_radius=self.border_radius[0],
            border_top_right_radius=self.border_radius[1],
            border_bottom_left_radius=self.border_radius[2],
            border_bottom_right_radius=self.border_radius[3]
        )
