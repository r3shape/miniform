from r3frame.globals import pg
from r3frame.utils import _asset_path
from r3frame.objects.game import Game_Object
from r3frame.application.ui import Interface
from r3frame.objects.world import Grid_Map, Quad_Map
from r3frame.application.resource import Window, Camera, Renderer, Asset_Manager

class Scene:
    def __init__(self, name: str, window_size: list[int], partition: Grid_Map|Quad_Map):
        self.name = name
        
        self.assets = Asset_Manager()
        
        self.window = Window(window_size, partition.size)
        pg.display.set_caption(name)
        pg.display.set_icon(pg.image.load(_asset_path("images/r3-logo.ico")))

        self.camera = Camera(self.window)
        self.renderer = Renderer(self.camera)
        self.interfaces = {}
        self.partition = partition

    def set_object(self, size: list[int], location: list[int|float], color: list[int]) -> Game_Object|None:
        obj = Game_Object(size, color, location)
        self.partition.set_cell(*location, obj)
        return obj
    def get_object(self, location: list[int|float]) -> None: return self.partition.get_cell(*location)
    def rem_object(self, location: list[int|float]) -> Game_Object|None: return self.partition.rem_cell(*location)

    def rem_interface(self, key: str) -> None:
        if self.get_interface(key) is not None: del self.interfaces[key]
    def get_interface(self, key: str) -> Interface|None: return self.interfaces.get(key, None)
    def set_interface(self, interface: Interface) -> None: self.interfaces[interface.name] = interface

    def handle_update(self) -> None:
        for interface in self.interfaces:
            self.interfaces[interface].update()
    
    def handle_render(self) -> None:
        for interface in self.interfaces:
            self.interfaces[interface].render()
