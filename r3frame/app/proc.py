from r3frame.globs import pg
from r3frame.atom import Atom

# ------------------------------------------------------------ #
class Process(Atom):
    def __init__(self, pid: int, app):
        super().__init__(pid, 0)
        self.app = app
        self._remove = lambda: self.app.processes.remove(self)

    def callback(self) -> bool: return False
    def fallback(self) -> None: self._remove()
# ------------------------------------------------------------ #
