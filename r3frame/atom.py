
# ------------------------------------------------------------ #
class Atom:
    def __init__(self, aid: int, flags: int) -> None:
        self._data = [aid, flags]

    def ID(self) -> int:    return self._data[0]
    def FLAGS(self) -> int: return self._data[1]

    def set_state(self, flag: int) -> None:
        self._data[1] |= flag

    def get_state(self, flag: int) -> bool:
        return ((self._data[1] & flag) == flag)

    def rem_state(self, flag: int) -> None:
        self._data[1] &= ~flag
# ------------------------------------------------------------ #
