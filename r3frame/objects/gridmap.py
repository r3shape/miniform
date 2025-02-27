from r3frame.utils import math
from r3frame.globals import pg

class GridMap:
    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.cells = []
        self.width = width
        self.height = height
        self.cell_size = cell_size

    def get_cell(self, x: int, y: int) -> None:
        try:
            return self.cells[y * self.width + x]
        except IndexError as err: return None
