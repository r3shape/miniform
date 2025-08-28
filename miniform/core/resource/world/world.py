from miniform.imports import pg, os, json
import miniform

from .tilemap import MiniTileMap
from .grid import MiniGridPartition
from .zone import MiniZonePartition
from .object import MiniStaticObject, MiniDynamicObject

class MiniWorld(miniform.MiniAtom):
    def __init__(
            self,
            app: "miniform.app.MiniApp",
            tile_map: MiniTileMap,
            partition: MiniGridPartition|MiniZonePartition) -> None:
        super().__init__()
        self.app: miniform.app.MiniApp = app
        self.cache: miniform.resource.MiniCache = app.cache

        self.configure(tile_map, partition)

    def configure(
            self,
            tile_map: MiniTileMap,
            partition: MiniGridPartition|MiniZonePartition) -> None:
        self.tile_map: miniform.resource.world.MiniTileMap = tile_map
        self.partition: miniform.resource.world.MiniGridPartition|miniform.resource.world.MiniZonePartition = partition
        self.light_proc: miniform.process.MiniLightProc = miniform.process.MiniLightProc(self.app, self.tile_map, self.partition)

        self.object_count: int = 0
        self.static_objects: list[miniform.resource.world.MiniStaticObject] = []
        self.dynamic_objects: list[miniform.resource.world.MiniDynamicObject] = []

    def init(self) -> None: raise NotImplementedError
    def exit(self) -> None: raise NotImplementedError

    def add_light(self, light: "miniform.resource.world.MiniLight") -> None:
        if not isinstance(light, miniform.resource.world.MiniLight): return
        self.light_proc.add_light(light)

    def load_object(
            self,
            key: str,
            size: list[int] = [8, 8],
            pos: list[float] = [0, 0],
            mass: float = 25.0,
            color: list[int] = [95, 205, 28],
            static: bool=True) -> MiniStaticObject|MiniDynamicObject:
            obj = self.cache.load_object(key, size, pos, mass, color, static)
            
            if static:
                self.static_objects.append(obj)
            else:
                self.dynamic_objects.append(obj)
            self.partition.add_object(obj)
            self.object_count += 1
            
            return obj
    
    def unload_object(self, key: str) -> None:
        obj = self.cache.get_object(key)
        self.rem_object(obj)

    def get_object(self, key: str) -> MiniStaticObject|MiniDynamicObject|None:
        return self.cache.get_object(key)

    def add_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        match obj.__class__:
            case miniform.resource.world.MiniStaticObject:
                self.static_objects.append(obj)
            case miniform.resource.world.MiniDynamicObject:
                self.dynamic_objects.append(obj)
            case _: return
        
        if obj.tag == None:
            obj.tag = f"obj-{self.object_count}"

        self.cache.store_object(obj.tag, obj)
        self.partition.add_object(obj)
        self.object_count += 1

    def rem_object(self, obj: MiniStaticObject|MiniDynamicObject) -> None:
        match obj.__class__:
            case miniform.resource.world.MiniStaticObject:
                self.static_objects.remove(obj)
            case miniform.resource.world.MiniDynamicObject:
                self.dynamic_objects.remove(obj)
            case _: return
        self.partition.rem_object(obj)
        self.cache.unload_object(obj.tag)
        self.object_count -= 1
    
    def update_hook(self, dt: float) -> None: pass
    def render_hook(self) -> None: pass
    
    def update(self, dt: float) -> None:
        urange = self.partition.query_cell_region(
                self.app.camera_proc.viewport_pos,
                self.app.camera_proc.viewport_size,
                xdir=5, ydir=5)
        for obj in urange:
            if obj.get_flag(miniform.MiniObjectFlag.OBJECT_STATIC): continue
            if any(obj.velocity):
                neighbors = self.partition.query_cell_region(obj.pos, obj.size, 1, 1)
                obj.update(neighbors, dt)
                self.partition.update_object(obj)
            obj.update_hook(dt)
        self.update_hook(dt)

        if self.tile_map.tile_count == 0:
            self.tile_map.tile_vertices = None

    def render(self) -> None:
        visible = self.partition.query_cell_region(
                self.app.camera_proc.viewport_pos,
                self.app.camera_proc.viewport_size,
                xdir=1, ydir=1)
        for obj in visible:
            self.app.render_proc.draw(obj.surface, obj.pos)
            obj.render_hook()
        self.render_hook()
