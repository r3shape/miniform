from r3frame.globs import pg
from r3frame.util import abs_path
from r3frame.app.ui.base import Interface
from r3frame.game import Tilemap, StaticPartition

# ------------------------------------------------------------ #
class Scene:
    def __init__(
            self, app, name: str,
            world_cellsize: int=32,
            world_size: list[int]=[200, 200],
            display_size: list[int]=[1600, 1200],
            interface_size: list[int]=[100, 100],
            display_color: list[int]=[203, 219, 252],
            interface_location: list[int]=[0, 0],
            font_path: str=abs_path("assets/fonts/megamax.ttf"),
    ) -> None:
        self.app = app
        self.name: str = name
        self.display_size: list[int] = display_size
        self.display_color: list[int] = display_color
        self.display: pg.Surface = pg.Surface(display_size)
        self.interface: Interface = Interface(
            name="scene interface",
            window=app.window,
            size=interface_size,
            location=interface_location,
            title_color=[255, 255, 255],
            font_path=font_path,
            text_color=[0, 0, 0],
            text_size=24,
        )


        self.world_size: list[int] = world_size
        self.world_cellsize: int = world_cellsize
        self.tilemap: Tilemap = Tilemap(app, world_size, world_cellsize)
        self.partition: StaticPartition = StaticPartition(world_size, world_cellsize)
        
        self.configure()

    def configure(self) -> None: ...
    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def handle_render(self) -> None: raise NotImplementedError
# ------------------------------------------------------------ #
