from miniform.imports import pg
import miniform

class MiniInterfaceProc(miniform.MiniAtom):
    def __init__(self, window) -> None:
        super().__init__()
        self.window: miniform.MiniWindow = window
        self.elements: dict[str, miniform.resource.interface.MiniElement] = {}

    def add_element(self, key: str, element) -> "miniform.resource.interface.MiniElement":
        if key in self.elements: return
        self.elements[key] = element
        miniform.MiniLogger.info(f"[MiniInterface] Set element: (key){key}")
        return element
    
    def get_element(self, key: str) -> "miniform.resource.interface.MiniElement":
        return self.elements.get(key, None)
    
    def rem_element(self, key: str) -> None:
        if key not in self.elements: return
        self.elements[key].parent = None
        del self.elements[key]
        miniform.MiniLogger.info(f"[MiniInterface] Removed element: (key){key}")

    def clear(self) -> None:
        for element in self.elements.values():
            element.parent = None
            element.clear()
        self.elements.clear()
        miniform.MiniLogger.info("[MiniInterface] Cleared all elements")

    def update(self, mouse, events) -> bool:
        def handle_element(element: miniform.resource.interface.MiniElement) -> bool:
            if not element.get_flag(miniform.MiniElementFlag.VISIBLE):
                return False

            if element.get_flag(miniform.MiniElementFlag.SHOW_ELEMENTS):
                for child in reversed(list(element.children.values())):
                    handle_element(child)

            element.on_update(events)
            if miniform.utils.point_inside(mouse.pos.screen, [*element.absolute_pos, *element.size]):
                mouse.Hovering = element
                if not element.get_flag(miniform.MiniElementFlag.HOVERED):
                    element.set_flag(miniform.MiniElementFlag.HOVERED)
                    element.on_hover()
                if events.mouse_pressed(mouse.LeftClick):
                    element.set_flag(miniform.MiniElementFlag.CLICKED)
                    element.on_click()
                else:
                    element.rem_flag(miniform.MiniElementFlag.CLICKED)
                return True
            else:
                mouse.Hovering = None
                if element.get_flag(miniform.MiniElementFlag.HOVERED):
                    element.rem_flag(miniform.MiniElementFlag.HOVERED)
                    element.on_unhover()
                if element.get_flag(miniform.MiniElementFlag.CLICKED):
                    if not events.mouse_pressed(mouse.LeftClick):
                        element.rem_flag(miniform.MiniElementFlag.CLICKED)
                return False

        for element in reversed(list(self.elements.values())):
            element._update_hook(mouse, events)
            if handle_element(element):
                return True
        return False
    
    def render(self) -> None:
        for element in self.elements.values():
            if isinstance(element, miniform.resource.interface.MiniContainer):
                element._layout()
            element._render(self.window.raster)
