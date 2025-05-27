from blakbox.globs import pg
from blakbox.atom import BOXatom
from blakbox.util import add_v2, sub_v2, point_inside

from blakbox.app.resource.inputs import BOXmouse
from blakbox.app.resource.window import BOXwindow
from blakbox.app.resource.events import BOXevents
from blakbox.app.ui.element import BOXelement, ELEMENT_FLAG

class INTERFACE_FLAG:
    SHOW_TITLE: int = (1 << 0)
    SHOW_ELEMENTS: int = (1 << 1)

# ------------------------------------------------------------ #
class BOXinterface(BOXatom):
    def __init__(self, pos: list[int] = [0, 0]) -> None:
        super().__init__(0, 0)
        
        # general settings
        self.pos: list[float] = pos
        self.title: str = "BOXinterface"
        self.title_color: list[int] = [0, 0, 0]
        
        self.elements: dict[str, BOXelement] = {}

        self.set_state(INTERFACE_FLAG.SHOW_ELEMENTS)

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

    def update(self, events: BOXevents, dt: float) -> None:
        if self.get_state(INTERFACE_FLAG.SHOW_ELEMENTS):
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
        if self.get_state(INTERFACE_FLAG.SHOW_TITLE):
            print("Show Interface Title")

        if self.get_state(INTERFACE_FLAG.SHOW_ELEMENTS):
            for elem in self.elements.values():
                window.screen.blit(elem.surface, elem.pos)
                elem.blit(window)
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