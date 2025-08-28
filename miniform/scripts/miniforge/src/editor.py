from .globals import miniform, pg

from .ui.footer import MiniFooter
from .ui.toolbar import MiniToolBar
from .ui.tilebar import MiniTileBar

class MiniEditor(miniform.resource.world.MiniWorld):
    def __init__(self, wf) -> None:
        super().__init__(
            app=wf,
            tile_map=miniform.resource.world.MiniTileMap(self, [16, 16], [0, 0], [50, 72, 60]),
            partition=miniform.resource.world.MiniGridPartition(wf, self, [16, 16], [0, 0])
        )

    def init(self) -> None:
        # SAVE STATE
        self.export_grid: bool = False

        # MAP SETTINGS
        self.map_name: str = "Map"
        self.map_path: str = "scripts/miniforge/external/.data/assets/map"

        # EDITOR STATE
        self.tile_id = 0
        self.tileset_id = 0
        self.tile_layer: int = 0
        self.tile_size = [16, 16]
        self.tile_origin = [0, 0]
        self.tile_color = [50, 72, 60]
        self.configure(
            tile_map=miniform.resource.world.MiniTileMap(self, self.tile_size, self.tile_origin, self.tile_color),
            partition=miniform.resource.world.MiniGridPartition(self.app, self, self.tile_size, self.tile_origin)
        )
        
        self.map_loaded: bool = 0
        self.tilebar_loaded: bool = 0

        self.theme: dict = self.app.theme
        self.map_pos: list[float] = [0.0, 0.0]

        # SCENE CONFIG
        self.app.interface_proc.add_element("footer", MiniFooter(self))
        self.app.interface_proc.add_element("tools", MiniToolBar(self))

        self.app.set_flag(miniform.MiniAppFlag.APP_DEBUG_TILE_MAP)

    def exit(self) -> None: pass

    def update_hook(self, dt: float) -> None:
        # map zoom
        if not isinstance(self.app.mouse.Hovering, miniform.resource.interface.MiniElement):
            self.app.camera_proc.zoom(-2 * self.app.events.mouse_wheel_up)
            self.app.camera_proc.zoom(2 * self.app.events.mouse_wheel_down)

        # map import
        if self.app.events.key_pressed(self.app.key_binds["import-map"]):
            if self.tile_map.import_data(self.map_name, miniform.utils._miniform_path(self.map_path)):
                self.map_loaded = True

        # map export
        if self.app.events.key_pressed(self.app.key_binds["export-map"]):
            self.tile_map.export_data(self.map_name, miniform.utils._miniform_path(self.map_path))

        # map image export
        if self.app.events.key_pressed(self.app.key_binds["export-map-image"]):
            self.tile_map.export_surface(self.map_name, self.map_path, self.export_grid)

        # map clear/reset
        if self.app.events.key_pressed(self.app.key_binds["clear-map"]):
            self.tile_map.clear()

        # set tile
        if not isinstance(self.app.mouse.Hovering, miniform.resource.interface.MiniElement)\
           and self.app.events.mouse_held(self.app.mouse_binds["set-tile"]):
            self.tile_map.set_tile(self.tile_layer, self.app.mouse.pos.view, self.tile_id, self.tileset_id)

        # rem tile
        if not isinstance(self.app.mouse.Hovering, miniform.resource.interface.MiniElement)\
           and self.app.events.mouse_held(self.app.mouse_binds["rem-tile"]):
            self.tile_map.rem_tile(self.tile_layer, self.app.mouse.pos.view)

        if self.map_loaded and not self.tilebar_loaded:
            self.app.interface_proc.add_element("tilebar", MiniTileBar(self))
            self.tilebar_loaded = 1
        elif not self.map_loaded:
            self.app.interface_proc.rem_element("tilebar")
            self.tilebar_loaded = 0

        self.cache.update_animation("load-anim", dt)

    def render_hook(self) -> None: pass
