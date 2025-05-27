
# ------------------------------------------------------------ #
class BOXatom:
    def __init__(self, aid: int, flags: int) -> None:
        self._data = [aid, flags]

    @property
    def id(self) -> int:    return self._data[0]

    @id.setter
    def id(self, id:int) -> None:   self._data[0] = id

    @property
    def flags(self) -> int: return self._data[1]

    def set_state(self, flag: int) -> None:
        self._data[1] |= flag

    def get_state(self, flag: int) -> bool:
        return ((self._data[1] & flag) == flag)

    def rem_state(self, flag: int) -> None:
        self._data[1] &= ~flag

    def sizeof(self) -> int:
        return self.__sizeof__()

    def copy(self) -> 'BOXatom':
        return BOXatom(self.id, self.flags)
# ------------------------------------------------------------ #
