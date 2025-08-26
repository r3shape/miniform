from miniform.imports import pg, math
import miniform

class MiniLightProc(miniform.MiniAtom):
    def __init__(
            self,
            app,
            partition):
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.partition: miniform.resource.world.MiniGridPartition|miniform.resource.world.MiniZonePartition = partition
        
        self.lights: list[miniform.resource.world.MiniLight] = []
        
        self.ray_size: int = 100
        self.ray_count: int = 164
        self.ray_sub_step:int = 4
        self.ray_step: float = 2 * math.pi / self.ray_count

    def add_light(self, light: "miniform.resource.world.MiniLight") -> None:
        if not isinstance(light, miniform.resource.world.MiniLight): return
        if light in self.lights: return
        self.lights.append(light)
    
    def cast_rays(self, light: "miniform.resource.world.MiniLight") -> None:
        r = light.radius
        center = light.pos

        for i in range(self.ray_count):
            angle = i * self.ray_step
            dx = math.cos(angle)
            dy = math.sin(angle)

            startx = center[0] + dx * r
            starty = center[1] + dy * r

            for step in range(0, self.ray_size, self.ray_sub_step):
                px = startx + dx * step
                py = starty + dy * step

                start = [startx, starty]
                end = [px, py]
                objs = self.partition.query_cell_region(end, [self.ray_sub_step, self.ray_sub_step], 1, 1)
                isec = False
                for obj in objs:
                    if pg.Rect(obj.rect).collidepoint(*end):
                        isec = True
                        break
                if isec: break
            light.rays.append([start, end])


    def render(self) -> None:
        render_proc = self.app.render_proc
        for light in self.lights:
            size = [light.radius + self.ray_size, light.radius + self.ray_size]
            pos = miniform.utils.sub_v2(light.pos, miniform.utils.scale_v2(size, .5))
            if not render_proc.visible(pos, size): continue
            
            light.rays.clear()
            self.cast_rays(light)
            render_proc.draw_circle(light.pos, light.radius, light.color)
            render_proc.draw_rect(size, pos, [255, 255, 255])
