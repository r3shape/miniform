from r3frame.utils import math
from r3frame.globals import pg
from r3frame.objects.game import Game_Object

class Grid_Map:
    def __init__(self, width: int, height: int, cell_size: int) -> None:
        self.cells = {}
        self.width = width                                  # in cells
        self.height = height                                # in cells
        self.cell_size = cell_size                          # in pixels
        self.size = [width * cell_size, height * cell_size] # in pixels

    def get_cell(self, x: int, y: int) -> Game_Object | None:
        """Returns the object at the given world (pixel) position."""
        gx, gy = x // self.cell_size, y // self.cell_size
        return self.cells.get((gx, gy), None)

    def set_cell(self, x: int, y: int, obj: Game_Object) -> None:
        """Places an object in the grid at the given world (pixel) position."""
        gx, gy = x // self.cell_size, y // self.cell_size
        self.cells[(gx, gy)] = obj
        obj.location = [gx * self.cell_size, gy * self.cell_size]

    def get_region(self, x: int, y: int) -> dict[str, Game_Object | None]:
        """Gets the object in the given cell and its immediate neighbors."""
        gx, gy = x // self.cell_size, y // self.cell_size
        directions = {
            "center": (0, 0),
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
            "left-up": (-1, -1),
            "right-up": (1, -1),
            "left-down": (-1, 1),
            "right-down": (1, 1),
        }
        return {dir_name: self.cells.get((gx + dx, gy + dy)) for dir_name, (dx, dy) in directions.items()}
