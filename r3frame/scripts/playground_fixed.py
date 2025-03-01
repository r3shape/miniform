import r3frame as frame
import random

play = frame.app.Application("Playground-Fixed", "Playground-Fixed", "GRID")

def load_assets() -> None:
    play.assets.load_image_sheet("run", frame.utils._asset_path("images/run.png"), [32, 32])
    play.assets.load_image_sheet("idle", frame.utils._asset_path("images/idle.png"), [32, 32])
    
    play.add_button("button_1", frame.utils._asset_path("fonts/megamax.ttf"), "Hello!", [200, 50], location=[5, 550], padding=[65, 16], text_size=16)
    button_1 = play.get_button("button_1")
    
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
play.load_assets = load_assets

def load_objects() -> None:
    play.player = frame.objects.game.Game_Object(
        mass=500, speed=150,
        location=[100, 100], color=[0, 0, 255],
    )

    play.player.set_animation("idle", play.assets.get_image("idle"), frame_duration=4)
    play.player.set_animation("run", play.assets.get_image("run"), frame_duration=5)

    def post_render():
        play.partition.render_debug(play.renderer, *[*map(int, [play.player.location[0] + play.player.size[0] / 2, play.player.location[1] + play.player.size[1] / 2])])
    play.renderer.post_render = post_render
play.load_objects = load_objects

def handle_events() -> None:
    zoom_factor = 3

    if play.events.key_pressed(frame.app.inputs.Keyboard.Escape): play.events.quit = 1

    if play.events.key_pressed(frame.app.inputs.Keyboard.F1): play.renderer.set_flag(play.renderer.FLAGS.SHOW_CAMERA)
    if play.events.key_pressed(frame.app.inputs.Keyboard.F2): play.renderer.rem_flag(play.renderer.FLAGS.SHOW_CAMERA)

    if play.events.key_held(frame.app.inputs.Keyboard.Down):    play.camera.set_velocity(vy=play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.Right):   play.camera.set_velocity(vx=play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.Left):    play.camera.set_velocity(vx=-play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.Up):      play.camera.set_velocity(vy=-play.player.speed)

    if play.events.mouse_wheel_up:
        play.camera.mod_viewport(-zoom_factor)

    if play.events.mouse_wheel_down:
        play.camera.mod_viewport(zoom_factor)

    if not isinstance(frame.app.inputs.Mouse.Hovering, frame.app.ui.Button) and play.events.mouse_held(frame.app.inputs.Mouse.LeftClick):
        mouse_location = frame.app.inputs.Mouse.get_location()
        world_x = (mouse_location[0] / play.camera.viewport_scale[0] + play.camera.location[0])
        world_y = (mouse_location[1] / play.camera.viewport_scale[1] + play.camera.location[1])
        play.partition.set_cell(world_x, world_y, frame.objects.game.Game_Object(
            size=[play.partition.cell_size, play.partition.cell_size],
            color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        ))

    if not isinstance(frame.app.inputs.Mouse.Hovering, frame.app.ui.Button) and play.events.mouse_pressed(frame.app.inputs.Mouse.RightClick):
        mouse_location = frame.app.inputs.Mouse.get_location()
        world_x = (mouse_location[0] / play.camera.viewport_scale[0] + play.camera.location[0])
        world_y = (mouse_location[1] / play.camera.viewport_scale[1] + play.camera.location[1])
        for o in play.partition.query_region(world_x, world_y, 1).values():
            if o:
                o.color = [255, 255, 255]
                o.set_image(None)

    if play.events.key_held(frame.app.inputs.Keyboard.W):       play.player.set_velocity(vy=-play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.S):       play.player.set_velocity(vy=play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.D):
        play.player.animation.flip_x =False
        play.player.set_velocity(vx=play.player.speed)
    if play.events.key_held(frame.app.inputs.Keyboard.A):
        play.player.animation.flip_x = True
        play.player.set_velocity(vx=-play.player.speed)
play.handle_events = handle_events

def handle_update() -> None:
    if play.player.velocity[0] != 0 or play.player.velocity[1] != 0:
        play.player.set_action("run")
    else:
        play.player.set_action("idle")

    play.player.update(play.clock.delta)
    for tile in play.partition.cells:
        if hasattr(tile, "update"): tile.update(play.clock.delta)

    play.camera.center_on(play.player.size, play.player.location)
play.handle_update = handle_update

def handle_render() -> None:
    [play.renderer.draw_call(o.image, o.location) for o in [*play.partition.cells.values(), play.player] if hasattr(o, "image")]
    
    play.dev.set_text_field("FPS", f"{play.clock.FPS:0.1f}", color=[0, 255, 0] if play.clock.FPS > play.clock.maxFPS/2 else [255, 0, 0])
    play.dev.set_text_field("OBJECTS", f"{len([*play.partition.cells, play.player])}")
    play.dev.set_text_field("DIRECTION", f"{play.player.get_facing()}")
    play.dev.set_text_field("VELOCITY", f"{play.player.velocity[0]:0.1f}, {play.player.velocity[1]:0.1f}")
    play.dev.set_text_field("LOCATION", f"{play.player.location[0]:0.1f}, {play.player.location[1]:0.1f}")
play.handle_render = handle_render

def playground(): play.run()
