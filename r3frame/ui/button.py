from r3frame.globs import pg

class Button:
    def __init__(self, font_path: str, text: str="Button", size: list[int]=[64, 64]) -> None:
        self.hovered = False
        self.show_border = False

        self.size = size
        self.location = [0, 0]
        self.image = pg.Surface(size)

        self.offset = [0, 0]
        self.padding: list[int] = [0, 0]
        self.color: list[int] = [0, 0, 0]

        self.border_size = [1, 1]
        self.border_radius = [0, 0, 0, 0]
        self.border_color = [255, 255, 255]

        self.text = text
        self.text_size: int = 18
        self.text_color: list[int] = [255, 255, 255]

        self.font_path = font_path
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
        if self.show_border:
            pg.draw.rect(surface, self.border_color, self.border(), width=self.border_size[0],
                border_top_left_radius=self.border_radius[0],
                border_top_right_radius=self.border_radius[1],
                border_bottom_left_radius=self.border_radius[2],
                border_bottom_right_radius=self.border_radius[3]
            )
