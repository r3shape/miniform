from blakbox.globs import pg, re
from blakbox.app.resource.clock import BOXclock
from blakbox.app.resource.events import BOXevents
from blakbox.app.resource.window import BOXwindow
from blakbox.app.resource.camera import BOXcamera
from blakbox.app.resource.object import BOXobject, OBJECT_FLAG
from blakbox.app.resource.surfatlas import BOXsurfatlas
from blakbox.app.resource.renderer import BOXrenderer, RENDERER_FLAG
from blakbox.app.resource.particle import BOXparticles
from blakbox.app.resource.inputs import BOXkeyboard, BOXmouse
from blakbox.app.resource.manager import BOXresources
from blakbox.app.resource.surface import BOXsurface
from blakbox.app.resource.surfarray import BOXsurfarray
from blakbox.app.resource.objectgrid import BOXobjectgrid
from blakbox.app.resource.tilemap import BOXtilemap


create_surface = lambda size, color: pg.Surface(size, pg.SRCALPHA)
create_rect = lambda location, size: pg.Rect(location, size)

fill_surface = lambda surface, color: surface.fill(color)
flip_surface = lambda surface, x, y: pg.transform.flip(surface, x, y)
scale_surface = lambda surface, scale: pg.transform.scale(surface, scale)
rotate_surface = lambda surface, angle: pg.transform.rotate(surface, angle)

blit_rect = lambda surface, rect, color, width: draw_rect(surface, rect.size, rect.topleft, color, width)
draw_line = lambda surface, start, end, color, width: pg.draw.line(surface, color, start, end, width=width)
draw_rect = lambda surface, size, location, color, width: pg.draw.rect(surface, color, pg.Rect(location, size), width=width)
draw_circle = lambda surface, center, radius, color, width: pg.draw.circle(surface, color, [*map(int, center)], radius, width)

def load_surface(path: str, scale: list[int] = None, color_key: list[int] = None) -> pg.Surface:
    surface = pg.image.load(path).convert_alpha()
    if color_key:
        surface.set_colorkey(color_key)
    if scale:
        surface = scale_surface(surface, scale)
    return surface

def surface_visible(surface: pg.Surface, threshold: int = 1) -> bool:
    pixels, transparent = 0, 0
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            if surface.get_at((x, y)).a == 0:
                transparent += 1
            pixels += 1
    return (pixels - transparent) >= threshold

def load_surface_sheet(sheet: pg.Surface, frame_size: list[int], scale: list[int] = None, color_key: list[int] = None) -> list[pg.Surface]:
    frames = []
    frame_x = sheet.get_width() // frame_size[0]
    frame_y = sheet.get_height() // frame_size[1]

    for row in range(frame_y):
        for col in range(frame_x):
            x = col * frame_size[0]
            y = row * frame_size[1]
            frame = pg.Surface(frame_size, pg.SRCALPHA).convert_alpha()
            if color_key:
                frame.set_colorkey(color_key)
            frame.blit(sheet, (0, 0), pg.Rect((x, y), frame_size))
            if scale:
                frame = scale_surface(frame, scale)
            frames.append(frame)
    return frames
def numeral_sort(strings: list[str]) -> list[str]:
    """this sorts strings like: 'img1.png', 'img2.png', 'img10.png'."""
    return sorted(strings, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)])

