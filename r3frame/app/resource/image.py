from r3frame.globs import pg
from r3frame.util import equal_arrays
from r3frame.app.resource.base import Resource

# ------------------------------------------------------------ #
class Image(Resource):
    def __init__(self, rid: int, data: pg.Surface, color: list[int]=[255, 255, 255]) -> None:
        super().__init__(rid, data)
        self.rotation: float = 0.0
        self.color: list[int] = color
        self.scale: list[float] = [1.0, 1.0]
        self.size: list[int] = [self.data.get_width(), self.data.get_height()]

    def fill(self, color: list[int]=None) -> None:
        if not isinstance(color, list): return
        if equal_arrays(self.color, color): return
        self.data.fill(color if color else self.color)
        self.color = color if color else self.color

    def scale(self, scale: list[float]) -> None:
        if not isinstance(scale, list): return
        if equal_arrays(self.scale, scale): return
        self.data = pg.transform.scale(self.data, [
            self.size[0] * scale[0],
            self.size[1] * scale[1]
        ])
        self.scale = scale
# ------------------------------------------------------------ #
