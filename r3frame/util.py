from r3frame.globs import os, math

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

def _asset_path(path: str) -> str:
    path = path.replace("/", os.sep).replace("\\", os.sep)
    return f"{__file__.removesuffix("util.py")}assets{os.sep}{path}"

def point_inside(point: list[int|float], bounds: list[int|float]) -> bool:
    return \
        point[0] > bounds[0] and point[0] < bounds[0] + bounds[2] \
    and point[1] > bounds[1] and point[1] < bounds[1] + bounds[3]

def dist_to(from_point: list[int|float], to_point: list[int|float]) -> list[float]:
    """Calculates a distance vector from two points."""
    return [
        to_point[0] - from_point[0],
        to_point[1] - from_point[1]
    ]

def angle_to(from_point: list[int|float], to_point: list[int|float]) -> float:
    """Calculates the angle (in degrees) between two points."""
    return math.degrees(math.atan2(*[
        to_point[0] - from_point[0],
        to_point[1] - from_point[1]
    ])) 


def bsort(data: list[int]) -> list[int]:
    for i in range(len(data)-1, 0, -1):
        for j in range(i):
            if data[j] > data[j+1]:
                temp = data[j]
                data[j] = data[j+1]
                data[j+1] = temp

