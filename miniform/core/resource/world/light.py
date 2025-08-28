from miniform.imports import math
import miniform

class MiniLight(miniform.MiniAtom):
    def __init__(
            self,
            pos: list[int|float],
            radius: int=16,
            color: list[int]=[255, 255, 50]) -> None:
        super().__init__()

        self.ray_len: int = 60
        self.radius: int = radius
        self.cell_radius: int = None
        self.rays: list[list[int]] = []
        self.pos: list[int|float] = pos
        self.color: list[int] = [*map(int, color)]

    def cast_rays(self, vertex_pair: list[list[int|float]]) -> None:
        self.rays.clear()
        if not vertex_pair: return

        for edge in vertex_pair:
            self.rays.append(edge[0])
            self.rays.append(edge[1])
