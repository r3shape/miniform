from miniform.imports import pg, re, os, math
import miniform

""" LAMBDAS """
lerp = lambda a, b, t: a + (b - a) * t
""" Simple Linear Interpolation"""

sine_wave_value = lambda A, B, t, C, D: int(A * math.sin((B * t) + C) + D)
"""
@brief Computes the y-coordinate of an oscillating motion following a sinusoidal (oscillatory, periodic, circular) wave.
@param A: Amplitude - The maximum height of the wave.
@param B: Frequency - Controls how fast the wave oscillates.
@param t: Time - Drives the motion forward.
@param C: Phase shift - Moves the wave left or right in time.
@param D: Vertical shift - Raises or lowers the wave.

@details
The function models a point’s vertical position as it moves in a circular or oscillatory path.
Mathematically, it returns the y-value of a sine wave:
    y = A * sin(B * t + C) + D
- The sine function describes smooth periodic motion.
- A larger amplitude (A) makes the oscillation taller.
- A higher frequency (B) makes it oscillate faster.
- The phase shift (C) offsets the wave horizontally.
- The vertical shift (D) moves the entire wave up/down.
"""

damp_exp = lambda x, factor, dt: x * (factor ** dt) if abs(x) > 0.01 else 0
"""
@brief Applies exponential damping to smoothly reduce a value over time.
@param x: The value to be damped (e.g., velocity, intensity, etc.).
@param factor: Damping factor (0 < factor < 1). Smaller values cause faster decay.
@param dt: Delta time (time step for decay application).

@details
This function simulates smooth, natural decay by multiplying `x` by a fractional factor:
    x_new = x * (factor ** dt)
- Works well for reducing velocity, smoothing animations, or applying drag-like effects.
- Ensures small values snap to 0 when they are close to stopping.
"""

damp_lin = lambda x, rate, threshold, dt: 0 if abs(x) < threshold else x - rate * dt * (1 if x > 0 else -1)
"""
@brief Applies linear damping to reduce a value at a fixed rate over time.
@param x: The value to be damped (e.g., velocity).
@param rate: The amount to reduce per second.
@param threshold: The stopping threshold (if |x| < threshold, it snaps to 0).
@param dt: Delta time (time step for decay application).

@details
This function simulates a linear friction effect by reducing `x` by a constant amount:
    x_new = x - rate * dt * sign(x)
- Good for simulating dry friction, velocity decay, or gradual slowdowns.
- Ensures the value stops completely when it gets close to 0.
"""

damp_linc = lambda c, x, rate, threshold, dt: c if abs(x) < threshold else x - rate * dt * (1 if x > c else -1)
"""
@brief Applies linear damping to reduce a value at a fixed rate over time.
@param c: The custom value to be dampened to.
@param x: The value to be damped (e.g., velocity).
@param rate: The amount to reduce per second.
@param threshold: The stopping threshold (if |x| < threshold, it snaps to 0).
@param dt: Delta time (time step for decay application).

@details
This function simulates a linear friction effect by reducing `x` by a constant amount:
    x_new = x - rate * dt * sign(x)
- Good for simulating dry friction, velocity decay, or gradual slowdowns.
- Ensures the value stops completely when it gets close to 0.
"""

# ------------------------------------------------------------ #
div_v2 = lambda v, s: [v[0] / s, v[1] / s]
div_v2i = lambda v, s: [*map(math.floor, [v[0] / s, v[1] / s])]
div2_v2 = lambda a, b: [a[0] / b[0], a[1] / b[1]]
div2_v2i = lambda a, b: [*map(math.floor, [a[0] // b[0], a[1] // b[1]])]
dist_v2 = lambda a, b: mag_v2(sub_v2(a, b))

scale_v2 = lambda v, s: [v[0] * s, v[1] * s]
scale_v2i = lambda v, s: [int(v[0] * s), int(v[1] * s)]

scale_v3 = lambda v, s: [v[0] * s, v[1] * s, v[2] * s]
scale_v3i = lambda v, s: [int(v[0] * s), int(v[1] * s), int(v[2] * s)]

mag_v2 = lambda v: (v[0]**2 + v[1]**2) ** 0.5

mul_v2 = lambda v, s: [v[0] * s[0], v[1] * s[1]]
mul_v2i = lambda v, s: [int(v[0] * s[0]), int(v[1] * s[1])]

add_v2 = lambda a, b: [a[0] + b[0], a[1] + b[1]]
sub_v2 = lambda a, b: [a[0] - b[0], a[1] - b[1]]
clamp = lambda v, l, u: l if v < l else u if v > u else v
equal_arrays = lambda a, b: all([*map(lambda a, b: a == b, a, b)])
unequal_arrays = lambda a, b: all([*map(lambda a, b: a != b, a, b)])
norm_v2 = lambda v: [v[0] / mag_v2(v), v[1] / mag_v2(v)] if mag_v2(v) != 0 else [0, 0]
# ------------------------------------------------------------ #

def _miniform_path(path: str, remcore: bool = 0) -> str:
    fp = __file__.split(os.sep)
    fp.remove(fp[-1])
    if remcore: fp.remove(fp[-1])
    [fp.append(p) for p in path.replace("/", os.sep).replace("\\", os.sep).split(os.sep)]
    return f"{os.sep}".join(fp)

def rel_path(path: str) -> str:
    fp = os.path.join(os.getcwd(), path.replace("/", os.sep).replace("\\", os.sep))
    return fp

def point_inside(point: list[int|float], bounds: list[int|float]) -> bool:
    return \
        point[0] > bounds[0] and point[0] < bounds[0] + bounds[2] \
    and point[1] > bounds[1] and point[1] < bounds[1] + bounds[3]

def bsort(data: list[int]) -> list[int]:
    for i in range(len(data)-1, 0, -1):
        for j in range(i):
            if data[j] > data[j+1]:
                temp = data[j]
                data[j] = data[j+1]
                data[j+1] = temp

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

def export_surface(name: str, path: str, surface: pg.Surface) -> None:
    path = rel_path(path)
    if not os.path.exists(path):
        miniform.MiniLogger.error(f"[Miniform] failed to export surface: (name){name} (path){path}")
        return False
    pg.image.save(surface, os.path.join(path, f"{name}.png"))
    miniform.MiniLogger.info(f"[Miniform] exported surface: (name){name} (path){path}")

def outline_surface(surface: pg.Surface, color: list[int] = [0, 0, 0], thickness: int = 1) -> pg.Surface:
    """ draws an outline by shifting the surface mask, and filling with the passed color """
    w, h = surface.get_size()
    outline_surface = pg.Surface([w + thickness * 2, h + thickness * 2], pg.SRCALPHA)
    outline_points = pg.mask.from_surface(surface).outline()

    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx == 0 and dy == 0: continue
            shifted_outline_points = [[x + dx + thickness, y + dy + thickness] for x, y in outline_points]
            pg.draw.polygon(outline_surface, color, shifted_outline_points, width=0)

    outline_surface.blit(surface, [thickness, thickness])
    return outline_surface

def palette_swap(surface: pg.Surface, swap_map: list[list[int]]) -> pg.Surface:
    result = surface.copy()
    pixels = pg.PixelArray(result)
    for src_color, swap_color in swap_map:
        print(src_color, swap_color)
        pixels.replace(surface.map_rgb(src_color), surface.map_rgb(swap_color))
    del pixels
    return result

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

def load_surface_array(path: str, frame_size: list[int], scale: list[int] = None, color_key: list[int] = None) -> list[pg.Surface]:
    sheet = load_surface(path, scale, color_key)
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
            if scale:
                frame = pg.transform.scale(frame, mul_v2(frame.size, scale))
            frame.blit(sheet, [0, 0], pg.Rect([x, y], frame_size))  # texture sampling :)
            frames.append(frame)
    return frames

def numeral_sort(strings: list[str]) -> list[str]:
    """this sorts strings like: 'img1.png', 'img2.png', 'img10.png'."""
    return sorted(strings, key=lambda s: [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s)])
