from miniform.imports import pg
import miniform

class MiniRenderProc(miniform.MiniAtom):
    def __init__(self, app: "miniform.app.MiniApp") -> None:
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.window: miniform.app.MiniWindow = app.window
        self.camera: miniform.process.MiniCameraProc = app.camera_proc
 
        self.blits: int = 0
        self.target: pg.Surface = pg.Surface(app.camera_proc.viewport_size, pg.SRCALPHA)

    def visible(self, pos: list[float], size: list[int]) -> bool:
        x, y = pos
        w, h = size
        vx, vy = self.camera.viewport_pos
        vw, vh = self.camera.viewport_size
        return x + w >= vx and x <= vx + vw and y + h >= vy and y <= vy + vh


    """ USER DRAWS """
    def draw(self, surface: pg.Surface, pos: list[float]) -> None:
        if self.visible(pos, surface.size):
            self.target.blit(surface, [*map(int, self.camera.project(pos))])
            self.blits += 1

    def draw_pixel(self, pos: list[int|float], color: list[int]=[255, 255, 255]) -> None:
        if self.visible(pos, [1, 1]):
            self.target.set_at(self.camera.project(pos), color)
            self.blits += 1

    def draw_line(self, start: list[int|float], end: list[int|float], color: list[int]=[255, 255, 255], width: int=1) -> None:
        if self.visible(start, [width, width]) or self.visible(end, [width, width]):
            pg.draw.line(self.target, color, self.camera.project(start), self.camera.project(end), width)
            self.blits += 1

    def draw_circle(self, center: list[int|float], radius: int, color: list[int]=[255, 255, 255], width: int=0) -> None:
        if self.visible(miniform.utils.sub_v2(center, [radius, radius]), miniform.utils.scale_v2([radius, radius], 2)):
            pg.draw.circle(self.target, color, self.camera.project(center), radius, width)

    def draw_rect(self, size: list[int], pos: list[int|float], color: list[int]=[255, 255, 255], width: int=1) -> None:
        if self.visible(pos, size):
            pg.draw.rect(self.target, color, pg.Rect([*map(int, self.camera.project(pos))], size), width=width)


    """ DEBUG DRAWS """
    def _debug_draw_zone_partition(self) -> None:
        if not isinstance(self.app.world, miniform.resource.world.world.MiniWorld): return
        
        partition = self.app.world.partition
        for zone_pos in partition.get_zone_region(self.app.camera_proc.viewport_pos, self.app.camera_proc.viewport_size):
            world_pos = miniform.utils.sub_v2(miniform.utils.mul_v2(zone_pos, partition.zone_size), partition.cell_origin)
            if not partition.query_zone(world_pos): continue

            self.draw_rect(partition.zone_size, world_pos, [0, 255, 0], 3)

            for cell_pos in partition.get_cell_region(world_pos, partition.zone_size, 1, 1):
                cell_origin = miniform.utils.sub_v2(miniform.utils.mul_v2(cell_pos, partition.cell_size), partition.cell_origin)
                if not partition.query_cell(cell_origin): continue

                self.draw_rect(partition.cell_size, cell_origin, [155, 155, 155], 1)

    def _debug_draw_grid_partition(self) -> None:
        if not isinstance(self.app.world, miniform.resource.world.world.MiniWorld): return

        partition = self.app.world.partition
        for cell_pos in partition.get_cell_region(
                self.app.camera_proc.viewport_pos,
                self.app.camera_proc.viewport_size,
                xdir=1, ydir=1):
            world_pos = miniform.utils.sub_v2(miniform.utils.mul_v2(cell_pos, partition.cell_size), partition.cell_origin)
            if not partition.query_cell(world_pos): continue
            self.draw_rect(partition.cell_size, world_pos, [0, 255, 0], 2)

    def _debug_draw_tile_map(self) -> None:
        if not isinstance(self.app.world, miniform.resource.world.world.MiniWorld): return

        tile_size = self.app.world.tile_map.tile_size
        
        start = [0, 0]
        end = [(start[0] * tile_size[0]) // tile_size[0],
               (start[1] * tile_size[1]) // tile_size[1]]
        
        for gx in range(int(start[0]), int(end[0])):
            x = gx * tile_size[0]
            self.draw_line([x, start[1] * tile_size[1]], [x, end[1] * tile_size[1]], [40, 40, 40], 1)
        
        for gy in range(int(start[1]), int(end[1])):
            y = gy * tile_size[1]
            self.draw_line([start[0] * tile_size[0], y], [end[0] * tile_size[0], y], [40, 40, 40], 1)

    def _debug_draw_light_rays(self) -> None:
        if not isinstance(self.app.world, miniform.resource.world.world.MiniWorld): return

        world = self.app.world
        lights = world.light_proc.lights
        for light in lights:
            for ray in light.rays:
                size = [light.radius + world.light_proc.ray_size, light.radius + world.light_proc.ray_size]
                pos = miniform.utils.sub_v2(light.pos, miniform.utils.scale_v2(size, .5))
                if not self.visible(pos, size): continue

                self.draw_line(ray[0], ray[1], light.color)
                self.draw_pixel(ray[1], [0, 255, 0])

    def update(self) -> None:
        self.blits = 0

        if self.app.get_flag(miniform.MiniAppFlag.APP_DEBUG_TILE_MAP):
            self._debug_draw_tile_map()
            
        if self.app.get_flag(miniform.MiniAppFlag.APP_DEBUG_PARTITION):
            match type(self.app.world.partition):
                case miniform.resource.world.MiniGridPartition:
                    self._debug_draw_grid_partition()
                case miniform.resource.world.MiniZonePartition:
                    self._debug_draw_zone_partition()
                case _: pass

        if isinstance(self.app.world, miniform.resource.world.world.MiniWorld):
            if self.app.get_flag(miniform.MiniAppFlag.APP_DEBUG_LIGHTS):
                self._debug_draw_light_rays()
            self.app.world.light_proc.render()

        self.window.draw(pg.transform.scale(self.target, self.window.size), [0, 0])

        if self.app.get_flag(miniform.MiniAppFlag.APP_DRAW_INTERFACE):
            self.app.interface_proc.render()

        if self.camera.get_flag(miniform.MiniCameraFlag.CAMERA_DIRTY):
            self.target = pg.Surface(self.camera.viewport_size, pg.SRCALPHA)
            self.camera.rem_flag(miniform.MiniCameraFlag.CAMERA_DIRTY)
        self.target.fill(self.window.color)
