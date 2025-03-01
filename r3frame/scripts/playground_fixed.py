import r3frame as frame
import random

class Playground(frame.app.Application):
    def __init__(self):
        super().__init__("Playground-Fixed")

    def load_assets(self) -> None:
        self.set_scene(frame.app.scene.Scene("Playground", [800, 600], frame.objects.world.Grid_Map(150, 150, 16)))
        
        self.active_scene.assets.load_image_sheet("run", frame.utils._asset_path("images/run.png"), [32, 32])
        self.active_scene.assets.load_image_sheet("idle", frame.utils._asset_path("images/idle.png"), [32, 32])
        
        self.active_scene.set_interface(frame.app.ui.Interface("Fun-Button", self.active_scene.window, [200, 50], [5, 550], frame.utils._asset_path("fonts/megamax.ttf")))
        self.active_scene.set_interface(frame.app.ui.Interface("Debug-Display", self.active_scene.window, [100, 100], [0, 0], frame.utils._asset_path("fonts/megamax.ttf")))
        
        self.active_scene.get_interface("Fun-Button").set_button("button_1", "Hello!", [200, 50], location=[5, 550], padding=[65, 16], text_size=16)
        button_1 = self.active_scene.get_interface("Fun-Button").get_button("button_1")
        
        def on_click() -> None:
            button_1.border_color = button_1.text_color = [
                random.randint(1, 255),
                random.randint(1, 255),
                random.randint(1, 255)
            ]
        def on_hover() -> None:
            button_1.text = "Click Me!"
            button_1.padding = [50, 16]
            button_1.border_color = button_1.text_color = [0, 255, 0]
        def on_unhover() -> None:
            button_1.text = "Hello!"
            button_1.padding = [65, 16]
            button_1.border_color = button_1.text_color = [255, 255, 255]
        button_1.on_click = on_click
        button_1.on_hover = on_hover
        button_1.on_unhover = on_unhover

    def load_objects(self) -> None:
        self.player = frame.objects.game.Game_Object(
            mass=500, speed=150,
            location=[100, 100], color=[0, 0, 255],
        )

        self.player.set_animation("idle", self.active_scene.assets.get_image("idle"), frame_duration=4)
        self.player.set_animation("run", self.active_scene.assets.get_image("run"), frame_duration=5)

        def post_render():
            self.active_scene.partition.render_debug(self.active_scene.renderer, *[*map(int, [self.player.location[0] + self.player.size[0] / 2, self.player.location[1] + self.player.size[1] / 2])])
        self.active_scene.renderer.post_render = post_render

    def handle_events(self) -> None:
        zoom_factor = 3

        if self.events.key_pressed(frame.app.inputs.Keyboard.Escape): self.events.quit = 1

        if self.events.key_pressed(frame.app.inputs.Keyboard.F1): self.active_scene.renderer.set_flag(self.active_scene.renderer.FLAGS.SHOW_CAMERA)
        if self.events.key_pressed(frame.app.inputs.Keyboard.F2): self.active_scene.renderer.rem_flag(self.active_scene.renderer.FLAGS.SHOW_CAMERA)

        if self.events.key_held(frame.app.inputs.Keyboard.Down):    self.active_scene.camera.set_velocity(vy=self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.Right):   self.active_scene.camera.set_velocity(vx=self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.Left):    self.active_scene.camera.set_velocity(vx=-self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.Up):      self.active_scene.camera.set_velocity(vy=-self.player.speed)

        if self.events.mouse_wheel_up:
            self.active_scene.camera.mod_viewport(-zoom_factor)

        if self.events.mouse_wheel_down:
            self.active_scene.camera.mod_viewport(zoom_factor)

        if not isinstance(frame.app.inputs.Mouse.Hovering, frame.app.ui.Button) and self.events.mouse_held(frame.app.inputs.Mouse.LeftClick):
            mouse_location = frame.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0])
            world_y = (mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1])
            self.active_scene.partition.set_cell(world_x, world_y, frame.objects.game.Game_Object(
                size=[self.active_scene.partition.cell_size, self.active_scene.partition.cell_size],
                color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
            ))

        if not isinstance(frame.app.inputs.Mouse.Hovering, frame.app.ui.Button) and self.events.mouse_held(frame.app.inputs.Mouse.RightClick):
            mouse_location = frame.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / self.active_scene.camera.viewport_scale[0] + self.active_scene.camera.location[0])
            world_y = (mouse_location[1] / self.active_scene.camera.viewport_scale[1] + self.active_scene.camera.location[1])
            for o in self.active_scene.partition.query_region(world_x, world_y, 1).values():
                if o:
                    self.active_scene.renderer.draw_rect(o.size, o.location, [0, 255, 0], 5)
                    self.active_scene.partition.rem_cell(*o.location)

        if self.events.key_held(frame.app.inputs.Keyboard.W):       self.player.set_velocity(vy=-self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.S):       self.player.set_velocity(vy=self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.D):
            self.player.animation.flip_x =False
            self.player.set_velocity(vx=self.player.speed)
        if self.events.key_held(frame.app.inputs.Keyboard.A):
            self.player.animation.flip_x = True
            self.player.set_velocity(vx=-self.player.speed)

    def handle_update(self) -> None:
        if self.player.velocity[0] != 0 or self.player.velocity[1] != 0:
            self.player.set_action("run")
        else:
            self.player.set_action("idle")

        self.player.update(self.clock.delta)
        for tile in self.active_scene.partition.cells:
            if hasattr(tile, "update"): tile.update(self.clock.delta)

        self.active_scene.camera.center_on(self.player.size, self.player.location)

    def handle_render(self) -> None:
        [self.active_scene.renderer.draw_call(o.image, o.location) for o in [*self.active_scene.partition.cells.values(), self.player] if hasattr(o, "image")]
        
        self.active_scene.get_interface("Debug-Display").set_text_field("FPS", f"{self.clock.FPS:0.1f}", color=[0, 255, 0] if self.clock.FPS > self.clock.maxFPS/2 else [255, 0, 0])
        self.active_scene.get_interface("Debug-Display").set_text_field("OBJECTS", f"{len([*self.active_scene.partition.cells, self.player])}")
        self.active_scene.get_interface("Debug-Display").set_text_field("DIRECTION", f"{self.player.get_facing()}")
        self.active_scene.get_interface("Debug-Display").set_text_field("VELOCITY", f"{self.player.velocity[0]:0.1f}, {self.player.velocity[1]:0.1f}")
        self.active_scene.get_interface("Debug-Display").set_text_field("LOCATION", f"{self.player.location[0]:0.1f}, {self.player.location[1]:0.1f}")

def playground(): Playground().run()
