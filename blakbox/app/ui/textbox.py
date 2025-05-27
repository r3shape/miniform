from blakbox.globs import pg
from blakbox.util import abs_path
from blakbox.app.ui.element import BOXelement

# ------------------------------------------------------------ #
class BOXtextbox(BOXelement):
    def __init__(
            self,
            size: list[int],
            text: str="BOXtextbox.text",
            text_size: int = 10,
            pos: list[int] = [0, 0],
            text_pos: list[int] = [0, 0],
            text_color: list[int] = [0, 0, 0],
            color: list[int] = [255, 255, 255],
            font_path: str = abs_path("assets/fonts/slkscr.ttf")
            ) -> None:
        super().__init__(size, pos, color)

        # general settings
        self.text: str = text
        self.text_size: int = text_size
        self.text_pos: list[int] = text_pos
        self.text_color: list[int] = text_color
        
        self._font_path: str = font_path
        self._font: pg.Font = pg.Font(self._font_path, self.text_size)

    def blit(self, window):
        self.surface.fill(self.color)
        self.surface.blit(self._font.render(self.text, True, self.text_color), self.text_pos)
        super().blit(window)
# ------------------------------------------------------------ #