"""Shared pixel geometry for native exports and visible-content checks."""

import math


def rotate_points(points, element, *, inverse=False):
    angle = math.radians(element.get("rotation", 0)) * (-1 if inverse else 1)
    if not angle:
        return list(points)
    x, y, w, h = element["box"]
    cx, cy = x + w / 2, y + h / 2
    c, s = math.cos(angle), math.sin(angle)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in points]


def box_points(box):
    x, y, w, h = box
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def polygon_points(element):
    x, y, w, h = element["box"]
    points = [(x + u * w, y + v * h) for u, v in element["vertices"]]
    # The clipping routine expects positive winding in screen coordinates.
    signed = sum(
        a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:] + points[:1], strict=True)
    )
    return points if signed > 0 else list(reversed(points))


def strictly_convex(vertices):
    direction = None
    for i, a in enumerate(vertices):
        b = vertices[(i + 1) % len(vertices)]
        for j, p in enumerate(vertices):
            if j in {i, (i + 1) % len(vertices)}:
                continue
            cross = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if abs(cross) <= 1e-9:
                return False
            if direction is None:
                direction = cross > 0
            elif (cross > 0) != direction:
                return False
    return True


def line_parts(element):
    (x1, y1), (x2, y2) = element["points"]
    length = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    half = max(element.get("stroke_width", 1), 0.1) / 2
    vx, vy = -uy, ux
    head = element.get("arrow_head")
    if head is None and element.get("arrow"):
        # Legacy Office heads vary by renderer; the SVG head gives conservative bounds.
        head = {"length": min(half * 12, length), "width": half * 12}
    bx, by = (x2 - ux * head["length"], y2 - uy * head["length"]) if head else (x2, y2)
    parts = [
        [
            (x1 - vx * half, y1 - vy * half),
            (bx - vx * half, by - vy * half),
            (bx + vx * half, by + vy * half),
            (x1 + vx * half, y1 + vy * half),
        ]
    ]
    if head:
        hw = head["width"] / 2
        parts.append([(bx - vx * hw, by - vy * hw), (x2, y2), (bx + vx * hw, by + vy * hw)])
    return parts


def arrow_outline(element):
    shaft, head = line_parts(element)
    return [shaft[0], shaft[1], head[0], head[1], head[2], shaft[2], shaft[3]]


def convex_hull(points):
    points = sorted(set(points))

    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    lower, upper = [], []
    for part, sequence in [(lower, points), (upper, reversed(points))]:
        for point in sequence:
            while len(part) > 1 and cross(part[-2], part[-1], point) <= 0:
                part.pop()
            part.append(point)
    return lower[:-1] + upper[:-1]
