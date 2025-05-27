from blakbox.globs import pg
from blakbox.atom import BOXatom
from blakbox.app.resource.inputs import BOXmouse
from blakbox.app.resource.events import BOXevents
from blakbox.app.resource.window import BOXwindow
from blakbox.util import add_v2, sub_v2, div_v2, point_inside

class ELEMENT_FLAG:
    HOVERED: int = (1 << 0)
    CLICKED: int = (1 << 1)
    SHOW_BORDER: int = (1 << 2)
    SHOW_ELEMENTS: int = (1 << 3)

# ------------------------------------------------------------ #
class BOXelement(BOXatom):
    def __init__(self, size: list[int], pos: list[float], color: list[int] = [255, 255, 255]) -> None:
        super().__init__(0, 0)
        
        self.size: list[int] = size
        self.pos: list[float] = pos
        self.color: list[int] = color
        self._offset: list[float] = [0, 0]

        self.border_width: int = 1
        self.border_size: list[int] = [0, 0]
        self.border_offset: list[int] = [0, 0]
        self.border_radius: list[int] = [0, 0, 0, 0]
        self.border_color: list[int] = [255, 255, 255]

        self.surface: pg.Surface = pg.Surface(self.size)
        self.surface.fill(self.color)

        self.elements: dict[str, BOXelement] = {}

        self.set_state(ELEMENT_FLAG.SHOW_ELEMENTS)

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(add_v2(self.pos, self._offset), self.size)

    @property
    def border(self) -> pg.Rect:
        return pg.Rect(sub_v2(add_v2(add_v2(self.pos, self._offset), self.border_offset), div_v2(self.border_size, 2)), add_v2(self.size, self.border_size))
    
    def set_element(self, key: str, element: "BOXelement") -> None:
        element.pos = [
            element.pos[0] + self.pos[0],
            element.pos[1] + self.pos[1]
        ]
        self.elements[key] = element
    
    def get_element(self, key: str) -> "BOXelement":
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if self.get_element(key) is not None:
            del self.elements[key]

    def on_click(self) -> None: pass
    def on_hover(self) -> None: pass
    def on_unhover(self) -> None: pass

    def update(self, events: BOXevents) -> None:
        if self.get_state(ELEMENT_FLAG.SHOW_ELEMENTS):
            for elem in self.elements.values():
                elem.update(events)
                mw = point_inside(BOXmouse.pos.screen, [*sub_v2(add_v2(elem.pos, elem._offset), elem.border_size), *add_v2(elem.size, elem.border_size)])
                if not elem.get_state(ELEMENT_FLAG.HOVERED) and mw:
                    BOXmouse.Hovering = BOXelement
                    elem.set_state(ELEMENT_FLAG.HOVERED)
                    elem.on_hover()
                if elem.get_state(ELEMENT_FLAG.HOVERED) and not mw:
                    BOXmouse.Hovering = None
                    elem.rem_state(ELEMENT_FLAG.HOVERED)
                    elem.on_unhover()
                if elem.get_state(ELEMENT_FLAG.HOVERED) and events.mouse_pressed(BOXmouse.LeftClick):
                    events.mouse[BOXmouse.LeftClick] = 0    # shouldnt need this but fixes the element double-click issue :|
                    elem.on_click()
                    
    def blit(self, window: BOXwindow) -> None:
        if self.get_state(ELEMENT_FLAG.SHOW_ELEMENTS):
            for elem in self.elements.values():
                elem.blit(window)
                window.screen.blit(elem.surface, elem.pos)
                elem._offset = self.pos
                if elem.get_state(ELEMENT_FLAG.SHOW_BORDER):
                    pg.draw.rect(
                        window.screen,
                        elem.border_color, elem.border, elem.border_width,
                        border_top_left_radius=elem.border_radius[0],
                        border_top_right_radius=elem.border_radius[1],
                        border_bottom_left_radius=elem.border_radius[2],
                        border_bottom_right_radius=elem.border_radius[3]
                    )
# ------------------------------------------------------------ #