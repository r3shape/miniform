from miniform.imports import pg
import miniform

from .element import MiniElement

class MiniLabel(MiniElement):
    def __init__(
            self,
            font: pg.Font,
            text: str = None,
            size: list[int] = None,
            icon: pg.Surface = None,
            icon_pos: list[float] = [0, 0],
            text_pos: list[float] = [0, 0],
            text_color: list[int] = [0, 0, 0],
            flags: int = 0,
            **kwargs
    ) -> None:
        super().__init__(size=font.size(text) if size is None else size, **kwargs)
        self.text: str = text
        self.font: pg.Font = font
        self.icon: pg.Surface = icon
        self.icon_pos: list[float] = icon_pos[:]
        self.text_pos: list[float] = text_pos[:]
        self.text_color: list[int] = text_color[:]
        self.text_set: list[str, list[float]] = []

        self.set_flag(miniform.MiniElementFlag.SHOW_TEXT)

    def set_text(self, text: str, pos: list[int|float], color: list[int]=None, border_color: list[int]=None, border_width: int=None) -> None:
        if not isinstance(text, str) or not miniform.utils.point_inside(miniform.utils.add_v2(pos, self.pos), [*self.pos, *self.size]): return
        self.text_set.append([
            text, pos,
            color if color else self.text_color,
            border_color if border_color else self.border_color,
            border_width if border_width else self.border_width
            ])

    def _render_hook(self, target: pg.Surface) -> None:
        if isinstance(self.text, str) and self.get_flag(miniform.MiniElementFlag.SHOW_TEXT):
            text_surf = self.font.render(self.text, self.get_flag(miniform.MiniElementFlag.ANTI_ALIAS), self.text_color)
            target.blit(text_surf, self.text_pos)

            for text, pos, color, bc, bw in self.text_set:
                text_surf = self.font.render(text, self.get_flag(miniform.MiniElementFlag.ANTI_ALIAS), color)
                target.blit(text_surf, pos)

                if self.get_flag(miniform.MiniElementFlag.SHOW_BORDER):
                    miniform.utils.draw_rect(target, text_surf.size, pos, bc, bw)
            self.text_set.clear()

        if isinstance(self.icon, pg.Surface):
            target.blit(self.icon, self.icon_pos)
