from miniform.imports import pg, math
import miniform

from ..resource.world.light import MiniLight
from ..resource.world.tilemap import MiniTileMap
from ..resource.world.grid import MiniGridPartition
from ..resource.world.zone import MiniZonePartition
from ..resource.world.object import MiniStaticObject, MiniDynamicObject

class MiniLightProc(miniform.MiniAtom):
    def __init__(
            self,
            app,
            tile_map,
            partition):
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.tile_map: MiniTileMap = tile_map
        self.partition: MiniGridPartition|MiniZonePartition = partition
        
        self.lights: list[MiniLight] = []

    def add_light(self, light: MiniLight) -> None:
        if not isinstance(light, MiniLight): return
        if light in self.lights: return
        self.lights.append(light)

    def light_phase(self, light: MiniLight, render_proc) -> list[MiniStaticObject|MiniDynamicObject]:
        light_size = miniform.utils.scale_v2([light.radius + light.ray_len, light.radius + light.ray_len], 2)
        light_pos = miniform.utils.sub_v2(light.pos, miniform.utils.scale_v2(light_size, .5))
        render_proc.draw_rect(light_size, light_pos, light.color, 1)
        if not render_proc.visible(light_pos, light_size): return

        cell_w, cell_h = self.partition.cell_size

        if not light.cell_radius:
            light.cell_radius = [(light_size[0] // cell_w) - 1, (light_size[1] // cell_h) - 1]

        light_rx = light_ry = light.radius
        light_crx, light_cry = light.cell_radius

        for cell in self.partition.get_cell_region(light.pos, [light_rx, light_ry], light_crx, light_cry):
            render_proc.draw_rect(self.partition.cell_size, miniform.utils.mul_v2(cell, self.partition.cell_size), [255, 0, 255], 1)

        # tile map pass
        light.cast_rays(self.tile_map.tile_vertices)        

    def shadow_phase(self, light: MiniLight, visible: list[MiniStaticObject|MiniDynamicObject], render_proc) -> None:
        if not visible: return
        else: return

    def render(self) -> None:
        render_proc = self.app.render_proc
        for light in self.lights:
            visible = self.light_phase(light, render_proc)
            self.shadow_phase(light, visible, render_proc)
            render_proc.draw_circle(light.pos, light.radius, light.color, 1)
            render_proc.draw_circle(light.pos, light.radius + light.ray_len, light.color, 1)
