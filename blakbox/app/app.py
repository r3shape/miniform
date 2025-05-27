from blakbox.globs import pg
from blakbox.atom import BOXatom
from blakbox.util import add_v2, div_v2

from blakbox.app.resource.clock import BOXclock
from blakbox.app.resource.events import BOXevents
from blakbox.app.resource.window import BOXwindow
from blakbox.app.resource.camera import BOXcamera
# from blakbox.app.ui.interface import BOXinterface
from blakbox.app.resource.renderer import BOXrenderer
from blakbox.app.resource.manager import BOXresources
from blakbox.app.resource.surfatlas import BOXsurfatlas
from blakbox.app.resource.inputs import BOXkeyboard, BOXmouse

from blakbox.app.scene import BOXscene

# ------------------------------------------------------------ #
class BOXapplication:
    def __init__(self, name: str="My App", window_size: list[int]=[800, 600], display_size: list[int]=[1600, 1200]) -> None:
        self.state: int = 0
        self.name:str = name
        self.clock: BOXclock = BOXclock()
        self.events: BOXevents = BOXevents()
        self.window: BOXwindow = BOXwindow(name, screen_size=window_size, display_size=display_size)

        self.scene: BOXscene = None
        self.scenev: list[BOXscene] = []

        self.configure()
    
    def add_scene(self, scene: BOXscene) -> int:
        id = len(self.scenev)
        self.scenev.append(scene)
        return id
    
    def set_scene(self, id: int) -> None:
        try:
            self.scene.cleanup()
            self.renderer.pre_render = lambda: None
            self.renderer.post_render = lambda: None
        except AttributeError as err: pass
        try:
            self.scene = self.scenev[id]
            self.scene.configure()
        except IndexError as err:
            print(f"Scene Not Found: (index){id}")

    def rem_scene(self, id: int) -> None:
        try:
            self.scenev.pop(id)
        except IndexError as err:
            print(f"Scene Not Found: (index){id}")

    def configure(self) -> None: raise NotImplementedError
    def handle_events(self) -> None: raise NotImplementedError
    def handle_update(self) -> None: raise NotImplementedError
    def cleanup(self) -> None: raise NotImplementedError

    def run(self) -> None:
        while not self.events.quit:
            self.clock.tick()
            self.window.clear()
            self.events.update()

            if isinstance(self.scene, BOXscene):
                self.handle_events()
                self.scene.handle_events()

                self.handle_update()
                self.scene.handle_update()
                self.scene.tilemap.grid.update()
                
                self.scene.camera.update(self.clock.delta)
                BOXmouse.pos.view = add_v2([BOXmouse.pos.screen[0] // self.scene.camera.viewport_scale[0],
                                            BOXmouse.pos.screen[1] // self.scene.camera.viewport_scale[1]], self.scene.camera.pos)
                
                self.scene.interface.update(self.events, self.clock.delta)
                self.scene.renderer.particles.update(self.clock.delta)

                self.scene.handle_render()
                self.scene.renderer.render()
                self.scene.interface.blit(self.window)
            else:
                self.handle_events()
                self.handle_update()
            
            BOXmouse.pos.rel = pg.mouse.get_rel()
            BOXmouse.pos.screen = pg.mouse.get_pos()
            BOXmouse.cursor.update(self.clock.delta)
            
            self.window.update()
            self.clock.rest()
        else:
            self.cleanup()
# ------------------------------------------------------------ #