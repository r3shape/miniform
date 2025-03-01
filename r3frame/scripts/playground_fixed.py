import r3frame as frame
import random

def playground():
    zoom_factor = 3

    clock = frame.app.resource.Clock()
    events = frame.app.events.Event_Manager()
    assets = frame.app.resource.Asset_Manager()
    
    gridmap = frame.objects.Grid_Map(1500, 1500, 8)
    window = frame.app.resource.Window([800, 600], gridmap.size)
    
    camera = frame.app.resource.Camera(window)
    renderer = frame.app.resource.Renderer(camera)

    dev = frame.app.resource.DevDisplay(
        f"r3frame {frame.version.R3FRAME_YEAR}.{frame.version.R3FRAME_MINOR}.{frame.version.R3FRAME_PATCH}",
        window, [100, 100], [0, 0], frame.utils._asset_path("fonts/megamax.ttf"), text_size=20)
    
    assets.load_image_sheet("run", frame.utils._asset_path("images/run.png"), [32, 32])
    assets.load_image_sheet("idle", frame.utils._asset_path("images/idle.png"), [32, 32])
    
    player = frame.objects.Game_Object(
        mass=500, speed=150,
        location=[100, 100], color=[0, 0, 255],
    )

    player.set_animation("idle", assets.get_image("idle"), frame_duration=4)
    player.set_animation("run", assets.get_image("run"), frame_duration=5)

    def post_render():
        gridmap.render_debug(renderer, *[*map(int, [player.location[0] + player.size[0] / 2, player.location[1] + player.size[1] / 2])])
    renderer.post_render = post_render

    while not events.quit:
        clock.update()
        events.update()

        if events.key_pressed(frame.app.inputs.Keyboard.Escape): events.quit = 1

        if events.key_pressed(frame.app.inputs.Keyboard.F1): renderer.set_flag(renderer.FLAGS.SHOW_CAMERA)
        if events.key_pressed(frame.app.inputs.Keyboard.F2): renderer.rem_flag(renderer.FLAGS.SHOW_CAMERA)

        if events.key_held(frame.app.inputs.Keyboard.Down):    camera.set_velocity(vy=player.speed)
        if events.key_held(frame.app.inputs.Keyboard.Right):   camera.set_velocity(vx=player.speed)
        if events.key_held(frame.app.inputs.Keyboard.Left):    camera.set_velocity(vx=-player.speed)
        if events.key_held(frame.app.inputs.Keyboard.Up):      camera.set_velocity(vy=-player.speed)

        if events.mouse_wheel_up:
            camera.mod_viewport(-zoom_factor)

        if events.mouse_wheel_down:
            camera.mod_viewport(zoom_factor)

        if events.mouse_held(frame.app.inputs.Mouse.LeftClick):
            mouse_location = frame.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / camera.viewport_scale[0] + camera.location[0])
            world_y = (mouse_location[1] / camera.viewport_scale[1] + camera.location[1])
            gridmap.set_cell(world_x, world_y, frame.objects.Game_Object(
                size=[gridmap.cell_size, gridmap.cell_size],
                color=[random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
            ))

        if events.mouse_pressed(frame.app.inputs.Mouse.RightClick):
            mouse_location = frame.app.inputs.Mouse.get_location()
            world_x = (mouse_location[0] / camera.viewport_scale[0] + camera.location[0])
            world_y = (mouse_location[1] / camera.viewport_scale[1] + camera.location[1])
            for o in gridmap.query_region(world_x, world_y, 1).values():
                if o:
                    o.color = [255, 255, 255]
                    o.set_image(None)

        if events.key_held(frame.app.inputs.Keyboard.S):       player.set_velocity(vy=player.speed)
        if events.key_held(frame.app.inputs.Keyboard.W):       player.set_velocity(vy=-player.speed)
        if events.key_held(frame.app.inputs.Keyboard.D):
            player.animation.flip_x =False
            player.set_velocity(vx=player.speed)
        if events.key_held(frame.app.inputs.Keyboard.A):
            player.animation.flip_x = True
            player.set_velocity(vx=-player.speed)
        
        if player.velocity[0] != 0 or player.velocity[1] != 0:
            player.set_action("run")
        else:
            player.set_action("idle")

        player.update(clock.delta)
        for tile in gridmap.cells:
            if hasattr(tile, "update"): tile.update(clock.delta)

        camera.center_on(player.size, player.location)
        camera.update(clock.delta)
        
        [renderer.draw_call(o.image, o.location) for o in [*gridmap.cells.values(), player] if hasattr(o, "image")]
        renderer.flush()

        dev.set_text_field("FPS", f"{clock.FPS:0.1f}", color=[0, 255, 0] if clock.FPS > clock.maxFPS/2 else [255, 0, 0])
        dev.set_text_field("OBJECTS", f"{len([*gridmap.cells, player])}")
        dev.set_text_field("DIRECTION", f"{player.get_facing()}")
        dev.set_text_field("VELOCITY", f"{player.velocity[0]:0.1f}, {player.velocity[1]:0.1f}")
        dev.set_text_field("LOCATION", f"{player.location[0]:0.1f}, {player.location[1]:0.1f}")
        dev.render()

        window.update()           
        clock.rest()
