from miniform.imports import time, functools
import miniform

def MiniProfile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000
        miniform.MiniLogger.debug(f"[Hprofile] {func.__qualname__} took {elapsed_ms:.3f} ms")
        return result
    return wrapper

class MiniAtom:
    def __init__(self) -> None:
        self._uid: int = id(self)
        self._flags: int = 0
        self._frozen: bool = 0

    @property
    def flags(self) -> int:
        return self._flags
    
    @property
    def uid(self) -> int:
        return self._uid

    def _freeze(self) -> None:
        if self._frozen == 1: return
        else: self._frozen = 1

    def _unfreeze(self) -> None:
        if self._frozen == 0: return
        else: self._frozen = 0

    def swap_flag(self, rem: int, set: int) -> None:
        self.rem_flag(rem)
        self.set_flag(set)

    def set_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._unfreeze()
        self._flags |= flag
        self._freeze()

    def get_flag(self, flag: int) -> bool:
        if flag < 0 or not isinstance(flag, int): return
        return ((self._flags & flag) == flag)

    def rem_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._unfreeze()
        self._flags &= ~flag
        self._freeze()
