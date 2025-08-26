import miniform

from .container import MiniContainer

class MiniScrollContainer(MiniContainer):
    def __init__(
            self,
            speed: int = 1,
            flags: int = 0,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)

        self.speed: int = speed
        self.scroll: list[int] = [0, 0]

        self.set_flag(flags)
    
    @property
    def scroll_bounds(self) -> list[int]:
        max_x, max_y = 0, 0
        for child in self.children.values():
            max_x = max(max_x, child.pos[0] + child.size[0])
            max_y = max(max_y, child.pos[1] + child.size[1])
        return [max_x, max_y]

    def _update_hook(self, mouse, events) -> None:
        if miniform.utils.point_inside(mouse.pos.screen, [*self.pos, *self.size]):
            self.scroll[1] = max(0, min(self.scroll_bounds[1], self.scroll[1] - events.wheel[1] * self.speed))

    def _layout(self, offset: list[int] = [0, 0]) -> None:
        super()._layout(miniform.utils.scale_v2(self.scroll, -1))
