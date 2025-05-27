import blakbox

# ------------------------------------------------------------ #
class BOXscene(blakbox.atom.BOXatom):
    def __init__(
            self, app,
            tile_size: list[int] = [32, 32],
            grid_size: list[int] = [50, 50],
            atlas_size: list[int] = [800, 600]
        ) -> None:
        super().__init__(0, 0)
        self.app: blakbox.app.BOXapplication = app
        self.interface: blakbox.app.ui.BOXinterface = blakbox.app.ui.BOXinterface()
        self.camera: blakbox.app.resource.BOXcamera = blakbox.app.resource.BOXcamera(app.window)
        self.resource: blakbox.app.resource.BOXresources = blakbox.app.resource.BOXresources(atlas_size)
        self.renderer: blakbox.app.resource.BOXrenderer = blakbox.app.resource.BOXrenderer(self, app.window, self.camera)
        self.tilemap: blakbox.app.resource.BOXtilemap = blakbox.app.resource.BOXtilemap(self, blakbox.util.scale_v2(tile_size, 2), grid_size)
        
    def cleanup(self) -> None: raise NotImplementedError
    def configure(self) -> None: raise NotImplementedError
    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError
# ------------------------------------------------------------ #