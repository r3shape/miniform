"""
Note: `configure()`, `cleanup()`, `handle_events()`, `handle_update()` and `handle_render()` must be defined for any instance of `BOXapplication` or `BOXscene`.

"""

import random
import blakbox

class FunButton(blakbox.app.ui.BOXtextbox):
    def __init__(self, app) -> None:
        super().__init__(
            size = [88, 32],
            color = [150, 150, 150],
            pos = [0, app.window.screen_size[1] - 32],

            text = "click",
            text_size = 18,
            text_pos = [16, 8],
            text_color = [0, 0, 0]
        )

        # configure base element
        self.border_width = 6
        self.border_size = [6, 6]
        self.border_radius = [10, 10, 10, 10]

        # configure state (atomic)
        self.set_state(blakbox.app.ui.ELEMENT_FLAG.SHOW_BORDER)

    def on_click(self):
        # define some on-click behavior
        self.border_color = [
            random.randint(1, 255),
            random.randint(1, 255),
            random.randint(1, 255)
        ]

    def on_hover(self):
        # define some on-hover behavior
        self.color = [80, 80, 80]
        self.text_color = [255, 255, 255]

    def on_unhover(self):
        # define some on-unhover behavior
        self.text_color = [0, 0, 0]
        self.color = [150, 150, 150]

class MainMenu(blakbox.app.BOXscene):
    def __init__(self, app) -> None:
        super().__init__(
            app = app,
            tile_size = [32, 32],   # expected size of world tiles
            grid_size = [50, 50],   # spatial partitioning grid size, the cell size is double that of the tiles to ensure spatial queries remain performant
            atlas_size = [800, 600] # the size of the surface used to store images in a single surface, instead of loading images over and over, they are blit from the atlas
        )

        # the BOXscene contains the BOXrenderer, which contains the BOXparticles system
        # lets add some particles to the cursor
        # first, configure a particle spawner
        # this function, like many others, also returns an integer ID representing the spawner
        self.particle_spawner = self.renderer.particles.set_spawner(
            pos = [0, 0],       # the position of this spawner, we'll modify this later
            rate = 4,           # how many particles per emission
            speed = 80,         # the speed at which particles are emitted
            lifetime = 0.8,     # the length of time particles exist for
            color = [0, 0, 0],  # the color of particles, we'll modify this later
            drange = [-2, -1],   # the range of directions this spawner can choose from (rot x and rot y)
            srange = [1, 4]    # the range of sizes this spawner can choose from 
        )

    def configure(self):
        # configure our window
        self.app.window.clear_color = [180, 180, 180]

        # configure our user interface
        self.interface.set_element("fun-button", FunButton(self.app))
        self.interface.set_element("fps", blakbox.app.ui.BOXtextbox(
            pos = [0, 0],
            size = [104, 32],
            color = [80, 80, 80],

            text_size = 18,
            text_pos = [8, 8],
            text_color = [255, 0, 0],
            text = f"FPS-{self.app.clock.fps:0.1f}",
        ))

    def cleanup(self): pass
    def handle_events(self): pass
    
    def handle_update(self):
        # lets modify our particle spawner from earlier to use a random color each frame,
        # also positioning the spawner at the mouse's location as seen by the camera (view space),
        # and randomizing the particle lifetimes a bit
        self.renderer.particles.mod_spawner(
            self.particle_spawner,
            pos = blakbox.app.resource.BOXmouse.pos.view,
            lifetime = random.choice([0.5, 0.3, 0.7, 0.2, 1.2, 1.5, 0.1, 1.8, 1.4, 2.5]),
            color = [
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)
            ]
        )

        # now lets tell the particle system to spawn particles
        self.renderer.particles.spawn()

        # lets also update the text for our FPS UI element
        if self.app.clock.fps >= 45.0:
            self.interface.get_element("fps").text_color = [0, 255, 0]
        else:
            self.interface.get_element("fps").text_color = [255, 0, 0]
        self.interface.get_element("fps").text = f"FPS-{self.app.clock.fps:0.1f}"
    
    def handle_render(self): pass

class MyGame(blakbox.app.BOXapplication):
    def __init__(self) -> None:
        super().__init__(
            name = "My Game",           # initial window title
            window_size = [800, 600],   # the window itself
            display_size = [1600, 1200] # the surface "within" the window 
        )

    def configure(self):
        # add our scene
        self.main_menu = self.add_scene(MainMenu(self))  # this returns an integer ID, representing our scene
        
        # we can use that integer ID to select our current scene
        self.set_scene(self.main_menu)

    def cleanup(self): pass
    def handle_events(self): pass
    def handle_update(self): pass

if __name__ == "__main__":
    MyGame().run()