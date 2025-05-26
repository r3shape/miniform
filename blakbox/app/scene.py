from blakbox.atom import BOXatom
from blakbox.app.resource.camera import BOXcamera
from blakbox.app.ui.interface import BOXinterface
from blakbox.app.resource.tilemap import BOXtilemap
from blakbox.app.resource.manager import BOXresources
from blakbox.app.resource.renderer import BOXrenderer

# ------------------------------------------------------------ #
class BOXscene(BOXatom):
    def __init__(
            self, app,
            tile_size: list[int] = [32, 32],
            grid_size: list[int] = [50, 50],
            atlas_size: list[int] = [800, 600]
        ) -> None:
        super().__init__(0, 0)
        self.app = app
        self.interface: BOXinterface = BOXinterface()
        self.camera: BOXcamera = BOXcamera(app.window)
        self.resource: BOXresources = BOXresources(atlas_size)
        self.tilemap: BOXtilemap = BOXtilemap(self, tile_size, grid_size)
        self.renderer: BOXrenderer = BOXrenderer(self, app.window, self.camera)
        
    def cleanup(self) -> None: raise NotImplementedError
    def configure(self) -> None: raise NotImplementedError
    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError
# ------------------------------------------------------------ #