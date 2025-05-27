import os, math


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
div_v2i = lambda v, s: [v[0] // s, v[1] // s]
div2_v2 = lambda a, b: [a[0] / b[0], a[1] / b[1]]
div2_v2i = lambda a, b: [a[0] // b[0], a[1] // b[1]]
dist_v2 = lambda a, b: mag_v2(sub_v2(a, b))
scale_v2 = lambda v, s: [v[0] * s, v[1] * s]
mag_v2 = lambda v: (v[0]**2 + v[1]**2) ** 0.5
mul_v2 = lambda v, s: [v[0] * s[0], v[1] * s[1]]
add_v2 = lambda a, b: [a[0] + b[0], a[1] + b[1]]
sub_v2 = lambda a, b: [a[0] - b[0], a[1] - b[1]]
clamp = lambda v, l, u: l if v < l else u if v > u else v
equal_arrays = lambda a, b: all([*map(lambda a, b: a == b, a, b)])
unequal_arrays = lambda a, b: all([*map(lambda a, b: a != b, a, b)])
norm_v2 = lambda v: [v[0] / mag_v2(v), v[1] / mag_v2(v)] if mag_v2(v) != 0 else [0, 0]
# ------------------------------------------------------------ #

def abs_path(path: str) -> str:
    fp = __file__.split(os.sep)
    fp.remove(fp[len(fp)-1])
    [fp.append(p) for p in path.replace("/", os.sep).replace("\\", os.sep).split(os.sep)]
    fp = f"{os.sep}".join(fp)
    return fp

def rel_path(path: str) -> str:
    fp = path.replace("/", os.sep).replace("\\", os.sep)
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