import r3frame as r3
import random

class Playground(r3.app.Application):
    def __init__(self):
        super().__init__("r3 playground")

    def load_assets(self) -> None:
        self.active_scene.assets.load_image("link", r3.utils._asset_path("images/link.png"), [16, 16])
        self.active_scene.assets.load_image("green-link", r3.utils._asset_path("images/green-link.png"), [16, 16])
        self.active_scene.assets.load_image_sheet("run", r3.utils._asset_path("images/run.png"), [32, 32])
        self.active_scene.assets.load_image_sheet("idle", r3.utils._asset_path("images/idle.png"), [32, 32])
        
    def load_scenes(self) -> None:
        self.set_scene(r3.app.scene.Scene("r3 playground", [800, 600], r3.objects.world.Grid_Map(150, 150, 16)))
        
        self.active_scene.set_interface(r3.app.ui.Interface("Debug", self.active_scene.window, [100, 100], [0, 0], r3.utils._asset_path("fonts/megamax.ttf")))
        
        self.active_scene.set_interface(r3.app.ui.Interface("Controls", self.active_scene.window, [200, 50], [5, 550], r3.utils._asset_path("fonts/megamax.ttf")))
        
        for i in range(4):
            self.active_scene.get_interface("Controls").set_button(f"button-{i+1}", f"Hello{i+1}!", [200, 50], location=[205 * i, 550], padding=[65, 16], text_size=16)

        button_1 = self.active_scene.get_interface("Controls").get_button("button-1")
        def on_click() -> None:
            button_1.text = random.choice(["Just Wow!", "Help Me!", "Hahaha!", "Not Funny!", "The Colors!", "Ouch!", "The Pain!", "r3frame!", "I Get It!", "OK!"])
            button_1.border_color = button_1.text_color = [
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)
            ]
            button_1.padding = [45, 16]
        def on_hover() -> None:
            button_1.text = "Click Me!"
            button_1.padding = [45, 16]
            button_1.border_color = button_1.text_color = [0, 255, 0]
        def on_unhover() -> None:
            button_1.text = "Hello!"
            button_1.padding = [65, 16]
            button_1.border_color = button_1.text_color = [255, 255, 255]
        button_1.on_click = on_click
        button_1.on_hover = on_hover
        button_1.on_unhover = on_unhover
    
    def load_objects(self) -> None:
        self.player = r3.objects.game.Game_Object(
            mass=500, speed=150,
            location=[100, 100], color=[0, 0, 255],
        )
        self.player.set_animation("idle", self.active_scene.assets.get_image("idle"), frame_duration=4)
        self.player.set_animation("run", self.active_scene.assets.get_image("run"), frame_duration=5)

        self.chain = r3.objects.game.Chain(r3.objects.game.Game_Object(color=[0, 255, 0], size=[16, 16], location=[100, 100]), [r3.objects.game.Game_Object(size=[16, 16], color=[255, 0, 0] if _+1 == 10 else [255, 255, 255]) for _ in range(10)], link_offset=[0, -8])
        for link in self.chain.links:
            link.set_image(self.active_scene.assets.get_image("link"))
        self.chain.root.set_image(self.active_scene.assets.get_image("green-link"))
        self.chain.get_scaling = lambda index, parent, link: 20
        self.chain.grabbed = False

        self.debug_mode = False
        def post_render():
            if self.debug_mode:
                self.active_scene.get_interface("Debug").name = "Debug - Active"
                self.chain.debug_render(self.active_scene.renderer)
                self.active_scene.partition.debug_render(self.active_scene.renderer, [*map(int, [self.player.location[0] + self.player.size[0] / 2, self.player.location[1] + self.player.size[1] / 2])])
                self.active_scene.get_interface("Debug").title_color = [0, 255, 0]
                self.active_scene.renderer.set_flag(self.active_scene.renderer.FLAGS.SHOW_CAMERA)
                self.active_scene.get_interface("Debug").set_text_field("FPS", f"{self.clock.FPS:0.1f}", color=[0, 255, 0] if self.clock.FPS > self.clock.maxFPS/2 else [255, 0, 0])
                self.active_scene.get_interface("Debug").set_text_field("OBJECTS", f"{len([*self.active_scene.partition.cells, self.player, *self.chain.get_objects()])}")
                self.active_scene.get_interface("Debug").set_text_field("DIRECTION", f"{self.player.get_facing()}")
                self.active_scene.get_interface("Debug").set_text_field("VELOCITY", f"{self.player.velocity[0]:0.1f}, {self.player.velocity[1]:0.1f}")
                self.active_scene.get_interface("Debug").set_text_field("LOCATION", f"{self.player.location[0]:0.1f}, {self.player.location[1]:0.1f}")
            else:
                self.active_scene.get_interface("Debug").name = "Debug - Inactive"
                self.active_scene.get_interface("Debug").title_color = [255, 0, 0]
                self.active_scene.renderer.rem_flag(self.active_scene.renderer.FLAGS.SHOW_CAMERA)
                self.active_scene.get_interface("Debug").rem_text_field("FPS")
                self.active_scene.get_interface("Debug").rem_text_field("OBJECTS")
                self.active_scene.get_interface("Debug").rem_text_field("DIRECTION")
                self.active_scene.get_interface("Debug").rem_text_field("VELOCITY")
                self.active_scene.get_interface("Debug").rem_text_field("LOCATION")
        self.active_scene.renderer.post_render = post_render

    def handle_events(self) -> None:
        zoom_factor = 3

        if self.events.key_pressed(r3.app.inputs.Keyboard.Escape): self.events.quit = 1

        if self.events.key_pressed(r3.app.inputs.Keyboard.F1): self.debug_mode = not self.debug_mode

        if self.events.key_held(r3.app.inputs.Keyboard.Down):    self.active_scene.camera.set_velocity(vy=self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.Right):   self.active_scene.camera.set_velocity(vx=self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.Left):    self.active_scene.camera.set_velocity(vx=-self.player.speed)
        if self.events.key_held(r3.app.inputs.Keyboard.Up):      self.active_scene.camera.set_velocity(vy=-self.player.speed)

        if self.events.mouse_wheel_up:
            self.active_scene.camera.mod_viewport(-zoom_factor)

        if self.events.mouse_wheel_down:
            self.active_scene.camera.mod_viewport(zoom_factor)

        if self.events.key_held(r3.app.inputs.Keyboard.E):
            mouse_location = r3.app.inputs.Mouse.get_location()
            wx, wy = [
                mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0],
                mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1],
            ]
            if r3.utils.point_inside([wx, wy], [*self.chain.root.location, *self.chain.root.size]):
                self.chain.grabbed = True
        else: self.chain.grabbed = False

        if not isinstance(r3.app.inputs.Mouse.Hovering, r3.app.ui.Button) and self.events.mouse_held(r3.app.inputs.Mouse.LeftClick):
            mouse_location = r3.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0])
            world_y = (mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1])
            self.active_scene.partition.set_cell(world_x, world_y, r3.objects.game.Game_Object(
                size=[self.active_scene.partition.cell_size, self.active_scene.partition.cell_size],
                color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
            ))

        if not isinstance(r3.app.inputs.Mouse.Hovering, r3.app.ui.Button) and self.events.mouse_held(r3.app.inputs.Mouse.RightClick):
            mouse_location = r3.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0])
            world_y = (mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1])
            for o in self.active_scene.partition.query_region(world_x, world_y, 1).values():
                if o:
                    self.active_scene.renderer.draw_rect(o.size, o.location, [0, 255, 0], 5)
                    self.active_scene.partition.rem_cell(*o.location)

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
                mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0],
                mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1],
            ]
        if self.player.velocity[0] != 0 or self.player.velocity[1] != 0:
            self.player.set_action("run")
        else:
            self.player.set_action("idle")

        self.player.update(self.clock.delta)
        for obj in self.active_scene.partition.cells.values():
            obj.update(self.clock.delta)

        self.active_scene.camera.center_on(self.player.size, self.player.location)

    def handle_render(self) -> None:
        [self.active_scene.renderer.draw_call(o.image, o.location) for o in [*self.active_scene.partition.cells.values(), self.player, *self.chain.get_objects()]]
        
def playground(): Playground().run()
