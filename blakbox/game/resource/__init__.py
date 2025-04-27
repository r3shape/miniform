from blakbox.globs import pg, re, os
from blakbox.game.resource.vfx import VFX
from blakbox.game.resource.image import Image
from blakbox.game.resource.surfmap import SurfMap
from blakbox.game.resource.animation import Animation
from blakbox.game.resource.particle import ParticleSystem

create_surface = lambda size, color: pg.Surface(size)
create_rect = lambda location, size: pg.Rect(location, size)

fill_surface = lambda surface, color: surface.fill(color)
flip_surface = lambda surface, x, y: pg.transform.flip(surface, x, y)
scale_surface = lambda surface, scale: pg.transform.scale(surface, scale)
rotate_surface = lambda surface, angle: pg.transform.rotate(surface, angle)

blit_rect = lambda rect, color, width: draw_rect(rect.size, rect.topleft, color, width)
draw_line = lambda surface, start, end, color, width: pg.draw.line(surface, color, start, end, width=width)
draw_rect = lambda surface, size, location, color, width: pg.draw.rect(surface, color, pg.Rect(location, size), width=width)
draw_circle = lambda surface, center, radius, color, width: pg.draw.circle(surface, color, [*map(int, center)], radius, width)

def flip_surface(surface: pg.Surface, x: bool, y: bool) -> pg.Surface:
    return pg.transform.flip(surface, x, y)

def scale_surface(surface: pg.Surface, scale: list[int]) -> pg.Surface:
    return pg.transform.scale(surface, scale)

def load_surface(path: str, scale: list[int] = None, color_key: list[int] = None) -> pg.Surface:
    surface = pg.image.load(path).convert_alpha()
    if color_key:
        surface.set_colorkey(color_key)
    if scale:
        surface = scale_surface(surface, scale)
    return surface

def image_visible(surface: pg.Surface, threshold: int = 1) -> bool:
    pixels, transparent = 0, 0
    for y in range(surface.get_height()):
        for x in range(surface.get_width()):
            if surface.get_at((x, y)).a == 0:
                transparent += 1
            pixels += 1
    return (pixels - transparent) >= threshold

def numeral_sort(strings: list[str]) -> list[str]:
    """this sorts strings like: 'img1.png', 'img2.png', 'img10.png'."""
    return sorted(strings, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)])

def extract_frames(sheet: pg.Surface, frame_size: list[int], scale: list[int] = None, color_key: list[int] = None) -> list[pg.Surface]:
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
