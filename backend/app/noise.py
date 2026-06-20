"""
Pure-Python value noise for procedural terrain generation.

Milestone 1:
  - value_noise_2d()   → single-octave coherent noise
  - fractal_noise()    → multi-octave layered noise (fBm)
  - No external dependencies (no `noise`, `opensimplex`, etc.)

Optimised for one-shot generation of a 50×50 grid at startup.
"""

import math


# ---------------------------------------------------------------------------
# Permutation table — a fixed shuffle of 0..255 used as a hash function
# to produce deterministic pseudo-random gradients from integer coords.
# Doubled to avoid index wrapping.
# ---------------------------------------------------------------------------

_PERM = [
    151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
    140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148,
    247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32,
    57, 177, 33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
    74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111, 229, 122,
    60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244, 102, 143, 54,
    65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169,
    200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64,
    52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212,
    207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213,
    119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
    129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104,
    218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241,
    81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106, 157,
    184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93,
    222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180,
]
_PERM = _PERM + _PERM  # double to avoid modulo wrapping


def _smoothstep(t: float) -> float:
    """Quintic smoothstep (Ken Perlin's improved curve)."""
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def _lerp(a: float, b: float, t: float) -> float:
    return a + t * (b - a)


def _hash_coord(ix: int, iy: int, seed: int) -> float:
    """Return a pseudo-random float in [0, 1) for integer grid point (ix, iy)."""
    # Combine coords with seed, then look up in permutation table
    h = _PERM[(_PERM[(ix + seed) & 255] + iy) & 255]
    return h / 255.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def value_noise_2d(x: float, y: float, seed: int = 0) -> float:
    """
    Compute 2D value noise at continuous coordinates (x, y).

    Returns a float in approximately [0, 1].
    Uses bilinear interpolation with quintic smoothstep.
    """
    # Integer cell coordinates
    ix = int(math.floor(x))
    iy = int(math.floor(y))

    # Fractional position within cell
    fx = x - ix
    fy = y - iy

    # Smooth the fractional parts
    sx = _smoothstep(fx)
    sy = _smoothstep(fy)

    # Hash the four corners of the cell
    n00 = _hash_coord(ix, iy, seed)
    n10 = _hash_coord(ix + 1, iy, seed)
    n01 = _hash_coord(ix, iy + 1, seed)
    n11 = _hash_coord(ix + 1, iy + 1, seed)

    # Bilinear interpolation
    nx0 = _lerp(n00, n10, sx)
    nx1 = _lerp(n01, n11, sx)
    return _lerp(nx0, nx1, sy)


def fractal_noise(
    x: float,
    y: float,
    octaves: int = 6,
    persistence: float = 0.5,
    scale: float = 1.0,
    seed: int = 0,
) -> float:
    """
    Fractal Brownian Motion (fBm) using layered value noise.

    Parameters
    ----------
    x, y        : World-space coordinates.
    octaves     : Number of noise layers (more = finer detail).
    persistence : Amplitude decay per octave (0–1).
    scale       : Base frequency (lower = larger features).
    seed        : RNG seed for reproducibility.

    Returns
    -------
    float in [0, 1] (normalised).
    """
    total = 0.0
    amplitude = 1.0
    frequency = scale
    max_value = 0.0  # for normalisation

    for i in range(octaves):
        total += value_noise_2d(x * frequency, y * frequency, seed + i * 31) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2.0

    # Normalise to [0, 1]
    return total / max_value if max_value > 0 else 0.0
