from r3frame.globs import pg

# ------------------------------------------------------------ #
class Resource:
    def __init__(self, rid: int=0, data=None) -> None:
        self.rid: int = rid
        self.data = data
        
    def sizeof(self) -> int:
        return self.__sizeof__()

    def copy(self) -> 'Resource':
        return self.__new__(Resource)
# ------------------------------------------------------------ #
