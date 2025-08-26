import miniform

from .element import MiniElement

class MiniContainer(MiniElement):
    class flags:
        # Layout Flags
        DISPLAY_ROW: int             = 1 << 15
        DISPLAY_LIST: int            = 1 << 16
        DISPLAY_ABSOLUTE: int        = 1 << 17
        
        # Alignment flags
        ALIGN_LEFT: int              = 1 << 18
        ALIGN_RIGHT: int             = 1 << 19
        ALIGN_CENTER: int            = 1 << 20

    def __init__(
            self,
            gap: int = 0,
            wrap_x: int = 1,
            wrap_y: int = 1,
            margin: list[int] = [0, 0],
            padding: list[int] = [0, 0],
            flags: int = 0,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._layout_warn: bool = False

        self.gap: int = gap
        self.wrap_x: int = int(wrap_x)    # max elements per row in DISPLAY_ROW
        self.wrap_y: int = int(wrap_y)    # max elements per column in DISPLAY_LIST
        self.margin: list[int] = margin[:]
        self.padding: list[int] = padding[:]

        self.set_flag(flags)
        self.set_flag(self.flags.DISPLAY_ROW)

    def _layout(self, offset: list[int] = [0, 0]) -> None:
        if not self.get_flag(self.flags.DISPLAY_ROW) and not self.get_flag(self.flags.DISPLAY_LIST) and not self.get_flag(self.flags.DISPLAY_ABSOLUTE):
            miniform.MiniLogger.warning("[Hcontainer] No layout flag set. Defaulting to DISPLAY_ABSOLUTE.")
            self.set_flag(self.flags.DISPLAY_ABSOLUTE)

        r, c = 0, 0
        w, h = 0, 0
        _offset = miniform.utils.add_v2(offset, miniform.utils.add_v2(self.padding, self.margin))
        for child in self.children.values():
            if self.get_flag(miniform.MiniElementFlag.DISPLAY_ABSOLUTE):
                return
            elif self.get_flag(miniform.MiniElementFlag.DISPLAY_ROW):
                if c >= self.wrap_x:
                    _offset[0] = offset[0] + self.padding[0] + self.margin[0]
                    _offset[1] += h + self.gap
                    c, w, h = 0, 0, 0

                child.pos = _offset[:]
                _offset[0] += child.size[0] + self.gap
                h = max(h, child.size[1])
                c += 1
            elif self.get_flag(miniform.MiniElementFlag.DISPLAY_LIST):
                if r >= self.wrap_y:
                    _offset[0] += w + self.gap
                    _offset[1] = offset[1] + self.padding[1] + self.margin[1]
                    r, w, h = 0, 0, 0

                child.pos = _offset[:]
                _offset[1] += child.size[1] + self.gap
                w = max(w, child.size[0])
                r += 1
