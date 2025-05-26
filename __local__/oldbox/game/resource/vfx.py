from oldbox.globs import pg
from oldbox.atom import Atom

# ------------------------------------------------------------ #
class VFX(Atom):
    def __init__(self, id: int, app) -> None:
        super().__init__()
        self.id: int = id
        self.app = app

    def update_render(self, surface: pg.Surface) -> None: raise NotImplementedError
# ------------------------------------------------------------ #
