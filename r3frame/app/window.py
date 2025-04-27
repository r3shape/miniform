from r3frame.globs import pg

# ------------------------------------------------------------ #
class Window:
    def __init__(self, size: list[int], display_size: list[int], color: list[int]=[25, 25, 25]) -> None:
        self.icon = None
        self.title = "HFWindow"
        self.size = size
        self.color = color
        self.clip_range = [1, 1]
        self.display_size = display_size
        self.window = pg.display.set_mode(size)
        
        self.blit_rect = lambda rect, color, width: self.draw_rect(rect.size, rect.topleft, color, width)
        self.draw_line = lambda start, end, color, width: pg.draw.line(self.display, color, start, end, width=width)
        self.draw_rect = lambda size, location, color, width: pg.draw.rect(self.display, color, pg.Rect(location, size), width=width)
        self.draw_circle = lambda center, radius, color, width: pg.draw.circle(self.display, color, [*map(int, center)], radius, width)
        self.configure(display_size)

    def set_title(self, title: str) -> None:
        self.title = title
        self.configure()

    def set_icon(self, icon: pg.Surface) -> None:
        self.icon = icon
        self.configure()

    def configure(self, display_size: list[int]) -> None:
        self.display_size = display_size
        self.display = pg.Surface(display_size)
        if isinstance(self.title, str): pg.display.set_caption(self.title)
        if isinstance(self.icon, pg.Surface): pg.display.set_icon(self.icon)

    def clear(self) -> None:
        self.display.fill(self.color)
        self.window.fill(self.color)

    def blit(self, surface: pg.Surface, location: list[int], offset: list[int]=[0, 0]) -> None:
        # display-culling
        if ((location[0] + surface.size[0]) - self.clip_range[0] < 0 or location[0] + self.clip_range[0] > self.display_size[0]) \
        or ((location[1] + surface.size[1]) - self.clip_range[1] < 0 or location[1] + self.clip_range[1] > self.display_size[1]):
            return
        self.display.blit(surface, [location[0] - offset[0], location[1] - offset[1]])

    def update(self) -> None:
        pg.display.flip()
# ------------------------------------------------------------ #
