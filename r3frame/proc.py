from .globs import pg

class Process:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def callback(self, data) -> bool: raise NotImplementedError
    def fallback(self, data) -> bool: raise NotImplementedError
