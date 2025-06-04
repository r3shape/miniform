from .globals import inspect
from .log import BOXlogger

def BOXprivate(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1].frame.f_globals.get("__name__")
        if not caller.startswith("blakbox."):
            BOXlogger.warning(f"Internal Method, cannot call `{func.__name__}`.")
            return
        return func(*args, **kwargs)
    return wrapper

class BOXatom:
    __slots__ = ("_mask", "_type", "_uid", "_frozen")

    def __init__(self) -> None:
        self._mask: int = 0
        self._type: int = 0
        self._uid: int = id(self)
        self._frozen: bool = False
        self._freeze()
    
    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False) and name in self.__slots__:
            BOXlogger.error(f"[BOXatom] This field is immutable, cannot assign: {self}.{name} = {value}")
            return
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if getattr(self, "_frozen", False) and name in self.__slots__:
            BOXlogger.error(f"[BOXatom] This field is immutable, cannot delete: (name){name}")
            return
        super().__delattr__(name)
    
    @BOXprivate
    def _freeze(self) -> None:
        if self._frozen == True:
            return
        self._frozen = True
    
    @BOXprivate
    def _unfreeze(self) -> None:
        if self._frozen == False:
            return
        self._frozen = False

    @property
    def frozen(self) -> bool:
        return self._frozen

    @property
    def mask(self) -> int:
        return self._mask
    
    @property
    def type(self) -> int:
        return self._type
    
    @property
    def uid(self) -> int:
        return self._uid

    def set_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._mask |= flag

    def get_flag(self, flag: int) -> bool:
        if flag < 0 or not isinstance(flag, int): return
        return ((self._mask & flag) == flag)

    def rem_flag(self, flag: int) -> None:
        if flag < 0 or not isinstance(flag, int): return
        self._mask &= ~flag

