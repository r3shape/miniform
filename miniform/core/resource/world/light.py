import miniform

class MiniLight(miniform.MiniAtom):
    def __init__(
            self,
            pos: list[int|float],
            radius: int=16,
            color: list[int]=[255, 255, 50]) -> None:
        super().__init__()

        self.radius: int = radius
        self.rays: list[list[int]] = []
        self.pos: list[int|float] = pos
        self.color: list[int] = [*map(int, color)]
