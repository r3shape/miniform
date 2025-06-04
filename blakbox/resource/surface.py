from blakbox.globals import pg
from blakbox.atom import BOXatom
from blakbox.utils import equal_arrays
from blakbox.resource.surfatlas import BOXsurfatlas

# ------------------------------------------------------------ #
class BOXsurface(BOXatom):
    def __init__(self, atlas_id: int, atlas_tag: str, path: str, size: list[int]) -> None:
        super().__init__(atlas_id, 0)
        self.path: str = path
        self.size: list[int] = size[:]
        self.atlas_tag: str = atlas_tag
        
    @property
    def data(self) -> list[int]:
        return [0, 0]
# ------------------------------------------------------------ #

