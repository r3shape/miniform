from miniform.imports import pg
import miniform

class MiniElement(miniform.MiniAtom):
    def __init__(
            self,
            pos: list[float] = [0, 0],
            size: list[int] = [10, 10],
            color: list[int] = [255, 255, 255],
            border_width: int = 1,
            border_color: list[int] = [0, 0, 0],
            border_radius: list[int] = [0, 0, 0, 0],
            flags: int = 0,
    ) -> None:
        super().__init__()
        self.size: list[int] = size[:]
        self.pos: list[float] = pos[:]
        self.color: list[int] = color[:]
        
        self.border_width: int = border_width
        self.border_color: list[int] = border_color[:]
        self.border_radius: list[int] = border_radius[:]

        self.parent: MiniElement = None
        self.children: dict[str, MiniElement] = {}

        self.surface: pg.Surface = pg.Surface(size, pg.SRCALPHA)
        self.surface.fill(color)

        self.set_flag(miniform.MiniElementFlag.VISIBLE)
        self.set_flag(miniform.MiniElementFlag.ANTI_ALIAS)
        self.set_flag(miniform.MiniElementFlag.SHOW_BORDER)
        self.set_flag(miniform.MiniElementFlag.SHOW_SURFACE)
        self.set_flag(miniform.MiniElementFlag.SHOW_ELEMENTS)
        
        self.set_flag(flags)

    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass
    def on_update(self, events) -> None: pass
    def on_render(self, surface: pg.Surface) -> None: pass

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.pos, self.size)

    @property
    def absolute_pos(self) -> list[float]:
        if self.parent:
            return miniform.utils.add_v2(self.pos, self.parent.absolute_pos)
        return self.pos[:]

    @property
    def absolute_rect(self) -> pg.Rect:
        return pg.Rect(self.absolute_pos, self.size)

    def set_element(self, key: str, element) -> None:
        if key in self.children: return
        element.parent = self
        self.children[key] = element
        miniform.MiniLogger.info(f"[MiniElement] Set child element: (key){key}")
    
    def get_element(self, key: str) -> "MiniElement":
        return self.children.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.children: return
        self.children[key].parent = None
        del self.children[key]
        miniform.MiniLogger.info(f"[MiniElement] Removed child element: (key){key}")

    def clear(self) -> None:
        for element in self.children.values():
            element.parent = None
            element.clear()
        self.children.clear()
        miniform.MiniLogger.info("[MiniElement] Cleared all child elements")

    def _update_hook(self, mouse, events) -> None: pass

    def _render_hook(self, target: pg.Surface) -> None: pass

    def _render(self, target: pg.Surface) -> None:
        if not self.get_flag(miniform.MiniElementFlag.VISIBLE):
            return

        if not self.get_flag(miniform.MiniElementFlag.SHOW_SURFACE):
            self.surface.fill(self.color+[0])
        else:
            self.surface.fill(self.color)

        if self.get_flag(miniform.MiniElementFlag.SHOW_ELEMENTS):
            for child in self.children.values():
                child._render(self.surface)
        
        self.on_render(self.surface)        # user render hook
        self._render_hook(self.surface)     # internal render hook
        target.blit(self.surface, self.pos)

        if self.get_flag(miniform.MiniElementFlag.SHOW_BORDER):
            pg.draw.rect(
                surface=target,
                rect=self.rect,
                color=self.border_color,
                width=self.border_width,
                border_top_left_radius=self.border_radius[0],
                border_top_right_radius=self.border_radius[1],
                border_bottom_left_radius=self.border_radius[2],
                border_bottom_right_radius=self.border_radius[3]
            )
