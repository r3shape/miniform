import r3frame as r3
import random

class Fun_Button(r3.app.ui.Button):
    def __init__(self) -> None:
        super().__init__(font_path=r3.utils._asset_path("fonts/megamax.ttf"), text="Hello!", size=[200, 50])
        self.show_border = True
        self.text_size = 16
        self.color = [0, 0, 0]
        self.padding = [65, 16]
        self.border_size = [5, 5]
        self.location = [195, 550]
        self.text_color = [255, 255, 255]

    def on_click(self) -> None:
        self.text = random.choice(["Just Wow!", "Help Me!", "Hahaha!", "Not Funny!", "The Colors!", "Ouch!", "The Pain!", "r3frame!", "I Get It!", "OK!"])
        self.border_color = self.text_color = [
            random.randint(1, 255),
            random.randint(1, 255),
            random.randint(1, 255)
        ]
        self.padding = [45, 16]

    def on_hover(self) -> None:
        self.text = "Click Me!"
        self.padding = [45, 16]
        self.border_color = self.text_color = [0, 255, 0]

    def on_unhover(self) -> None:
        self.text = "Hello!"
        self.padding = [65, 16]
        self.border_color = self.text_color = [255, 255, 255]

class Debug_Button(r3.app.ui.Button):
    def __init__(self, app: r3.app.Application) -> None:
        super().__init__(font_path=r3.utils._asset_path("fonts/megamax.ttf"), text="Debug", size=[200, 50])
        self.app = app
        self.text_size = 16
        self.show_border = True
        self.color = [0, 0, 0]
        self.padding = [65, 16]
        self.border_size = [5, 5]
        self.location = [400, 550]
        self.text_color = [255, 0, 0] if not self.app.debug_mode else [0, 255, 0]
        self.border_color = [255, 0, 0] if not self.app.debug_mode else [0, 255, 0]

    def on_click(self) -> None:
        self.app.debug_mode = not self.app.debug_mode
        self.text_color = [255, 0, 0] if not self.app.debug_mode else [0, 255, 0]
        self.border_color = [255, 0, 0] if not self.app.debug_mode else [0, 255, 0]
    
    def on_hover(self) -> None:
        self.border_color = [255, 255, 255]
    
    def on_unhover(self) -> None:
        self.border_color = [255, 0, 0] if not self.app.debug_mode else [0, 255, 0]

class Interact_Tip(r3.app.ui.Tooltip):
    def __init__(self) -> None:
        super().__init__(
            size=[150, 64],
            text='Press\n"Interact"',
            font_path=r3.utils._asset_path("fonts/megamax.ttf")
        )
        self.show_border = True
        self.padding = [5, 5]
        self.offset = [10, -10]
        self.location = r3.app.inputs.Mouse.get_location()

class Playground(r3.app.Application):
    def __init__(self):
        super().__init__("r3 playground")
        self.debug_mode = False

    def load_assets(self) -> None:
        self.assets.load_image("link", r3.utils._asset_path("images/link.png"), [16, 16])
        self.assets.load_image("green-link", r3.utils._asset_path("images/green-link.png"), [16, 16])
        self.assets.load_image_sheet("run", r3.utils._asset_path("images/run.png"), [32, 32])
        self.assets.load_image_sheet("idle", r3.utils._asset_path("images/idle.png"), [32, 32])
        
    def load_scenes(self) -> None:
        self.set_scene(r3.app.scene.Scene("r3 playground", r3.objects.world.Grid_Map(150, 150, 16)))
        
        self.active_scene.set_interface(r3.app.ui.Interface("Debug", self.window, [100, 100], [0, 0], r3.utils._asset_path("fonts/megamax.ttf")))
        self.active_scene.set_interface(r3.app.ui.Interface("Buttons", self.window, [200, 50], [5, 550], r3.utils._asset_path("fonts/megamax.ttf")))
        
        self.active_scene.get_interface("Buttons").show_name = False
        self.active_scene.get_interface("Buttons").set_button("button-1", Fun_Button())
        self.active_scene.get_interface("Buttons").set_button("button-2", Debug_Button(self))
    
        self.active_scene.set_interface(r3.app.ui.Interface("Controls", self.window, [200, 50], [600, 5], r3.utils._asset_path("fonts/megamax.ttf")))
        self.active_scene.get_interface("Controls").set_text_field("Up", "W", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Down", "S", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Left", "A", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Right", "D", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Interact", "E", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Place", "L-Click", [200, 200, 200])
        self.active_scene.get_interface("Controls").set_text_field("Remove", "R-Click", [200, 200, 200])

    def load_objects(self) -> None:
        self.player = r3.objects.game.Game_Object(
            mass=500, speed=150,
            location=[100, 100], color=[0, 0, 255],
        )
        self.player.set_animation("idle", self.assets.get_image("idle"), frame_duration=4)
        self.player.set_animation("run", self.assets.get_image("run"), frame_duration=5)

        self.chain = r3.objects.game.Chain(r3.objects.game.Game_Object(color=[0, 255, 0], size=[16, 16], location=[100, 100]), [r3.objects.game.Game_Object(size=[16, 16], color=[255, 0, 0] if _+1 == 10 else [255, 255, 255]) for _ in range(10)], link_offset=[0, -8])
        for link in self.chain.links:
            link.set_image(self.assets.get_image("link"))
        self.chain.root.set_image(self.assets.get_image("green-link"))
        self.chain.get_scaling = lambda index, parent, link: 20
        self.chain.grabbed = False

        def post_render():
            if self.debug_mode:
                self.active_scene.get_interface("Debug").name = "Debug - Active"
                self.chain.debug_render(self.renderer)
                self.active_scene.partition.debug_render(self.renderer, [*map(int, [self.player.location[0] + self.player.size[0] / 2, self.player.location[1] + self.player.size[1] / 2])])
                self.active_scene.get_interface("Debug").title_color = [0, 255, 0]
                self.renderer.set_flag(self.renderer.FLAGS.SHOW_CAMERA)
                self.active_scene.get_interface("Debug").set_text_field("FPS", f"{self.clock.FPS:0.1f}", color=[0, 255, 0] if self.clock.FPS > self.clock.maxFPS/2 else [255, 0, 0])
                self.active_scene.get_interface("Debug").set_text_field("OBJECTS", f"{len([*self.active_scene.partition.cells, self.player, *self.chain.get_objects()])}")
                self.active_scene.get_interface("Debug").set_text_field("DIRECTION", f"{self.player.get_facing()}")
                self.active_scene.get_interface("Debug").set_text_field("VELOCITY", f"{self.player.velocity[0]:0.1f}, {self.player.velocity[1]:0.1f}")
                self.active_scene.get_interface("Debug").set_text_field("LOCATION", f"{self.player.location[0]:0.1f}, {self.player.location[1]:0.1f}")
            else:
                self.active_scene.get_interface("Debug").name = "Debug - Inactive"
                self.active_scene.get_interface("Debug").title_color = [255, 0, 0]
                self.renderer.rem_flag(self.renderer.FLAGS.SHOW_CAMERA)
                self.active_scene.get_interface("Debug").rem_text_field("FPS")
                self.active_scene.get_interface("Debug").rem_text_field("OBJECTS")
                self.active_scene.get_interface("Debug").rem_text_field("DIRECTION")
                self.active_scene.get_interface("Debug").rem_text_field("VELOCITY")
                self.active_scene.get_interface("Debug").rem_text_field("LOCATION")
        self.renderer.post_render = post_render

    def handle_events(self) -> None:
        zoom_factor = 3

        if self.events.key_pressed(r3.app.inputs.Keyboard.Escape): self.events.quit = 1

        if self.events.mouse_wheel_up:
            self.camera.mod_viewport(-zoom_factor)

        if self.events.mouse_wheel_down:
            self.camera.mod_viewport(zoom_factor)

        mouse_location = r3.app.inputs.Mouse.get_location()
        mouse_world_location = [
            mouse_location[0] / self.camera.viewport_scale[0] + self.camera.location[0],
            mouse_location[1] / self.camera.viewport_scale[1] + self.camera.location[1],
        ]

        if r3.utils.point_inside([mouse_world_location[0], mouse_world_location[1]], [*self.chain.root.location, *self.chain.root.size]):
            self.active_scene.get_interface("Controls").set_tooltip("interact", Interact_Tip())
            if self.events.key_held(r3.app.inputs.Keyboard.E):
                self.chain.grabbed = True
                self.active_scene.get_interface("Controls").rem_tooltip("interact")
            else: self.chain.grabbed = False
        else:
            self.active_scene.get_interface("Controls").rem_tooltip("interact")

        if not isinstance(r3.app.inputs.Mouse.Hovering, r3.app.ui.Button) and self.events.mouse_held(r3.app.inputs.Mouse.LeftClick):
            self.active_scene.partition.set_cell(mouse_world_location[0], mouse_world_location[1], r3.objects.game.Game_Object(
                size=[self.active_scene.partition.cell_size, self.active_scene.partition.cell_size],
                color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
            ))

        if not isinstance(r3.app.inputs.Mouse.Hovering, r3.app.ui.Button) and self.events.mouse_held(r3.app.inputs.Mouse.RightClick):
            self.active_scene.partition.rem_cell(mouse_world_location[0], mouse_world_location[1])

        if self.events.key_held(r3.app.inputs.Keyboard.W):       self.player.set_velocity(vy=-self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.S):       self.player.set_velocity(vy=self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.D):
            self.player.animation.flip_x =False
            self.player.set_velocity(vx=self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.A):
            self.player.animation.flip_x = True
            self.player.set_velocity(vx=-self.player.speed)

    def handle_update(self) -> None:
        self.chain.update(self.clock.delta)
        if self.chain.grabbed:
            mouse_location = r3.app.inputs.Mouse.get_location()
            self.chain.root.location = [
                (mouse_location[0] / self.camera.viewport_scale[0] + self.camera.location[0]) - self.chain.root.size[0] / 2,
                (mouse_location[1] / self.camera.viewport_scale[1] + self.camera.location[1]) - self.chain.root.size[1] / 2,
            ]
        if self.player.velocity[0] != 0 or self.player.velocity[1] != 0:
            self.player.set_action("run")
        else:
            self.player.set_action("idle")

        self.player.update(self.clock.delta)
        for obj in self.active_scene.partition.cells.values():
            obj.update(self.clock.delta)

        self.camera.center_on(self.player.size, self.player.location)

    def handle_render(self) -> None:
        [self.renderer.draw_call(o.image, o.location) for o in [*self.active_scene.partition.cells.values(), self.player, *self.chain.get_objects()]]
        
def playground(): Playground().run()
