"""Oklab differences for normalized, 8-bit sRGB core colors.

Equations: Björn Ottosson, https://bottosson.github.io/posts/oklab/
Linear-sRGB matrices are offered by the author as public domain.
This is ΔEOK (0–1 lightness), not CIE ΔE2000 or HSV saturation.
"""

import math


def oklab(rgb):
    channels = [v / 255 for v in rgb]
    r, g, b = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    cone_l = math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return (
        0.2104542553 * cone_l + 0.7936177850 * m - 0.0040720468 * s,
        1.9779984951 * cone_l - 2.4285922050 * m + 0.4505937099 * s,
        0.0259040371 * cone_l + 0.7827717662 * m - 0.8086757660 * s,
    )


def color_difference(expected, actual):
    a, b = oklab(expected), oklab(actual)
    return {
        "metric": "delta_e_ok",
        "expected_oklab": list(a),
        "actual_oklab": list(b),
        "delta_e_ok": math.dist(a, b),
        "lightness_change": b[0] - a[0],
        "chroma_change": math.hypot(*b[1:]) - math.hypot(*a[1:]),
    }
