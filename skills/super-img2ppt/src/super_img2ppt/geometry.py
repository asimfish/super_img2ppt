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


def _cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def triangulate(vertices):
    """Validate one simple contour and partition its actual interior for QA."""
    points = [tuple(p) for p in vertices]
    if len(set(points)) != len(points):
        raise ValueError("Freeform vertices must be distinct")
    # Remove redundant points, retaining backtracking edges for rejection below.
    changed = True
    while changed and len(points) > 3:
        changed = False
        for i, b in enumerate(points):
            a, c = points[i - 1], points[(i + 1) % len(points)]
            if abs(_cross(a, b, c)) <= 1e-12 and (
                (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1]) > 0
            ):
                points.pop(i)
                changed = True
                break
    edges = list(zip(points, points[1:] + points[:1], strict=True))
    for i, (a, b) in enumerate(edges):
        for j in range(i + 1, len(edges)):
            if j == i + 1 or (i == 0 and j == len(edges) - 1):
                continue
            c, d = edges[j]
            if (
                max(min(a[0], b[0]), min(c[0], d[0]))
                <= min(max(a[0], b[0]), max(c[0], d[0])) + 1e-12
                and max(min(a[1], b[1]), min(c[1], d[1]))
                <= min(max(a[1], b[1]), max(c[1], d[1])) + 1e-12
                and _cross(a, b, c) * _cross(a, b, d) <= 1e-24
                and _cross(c, d, a) * _cross(c, d, b) <= 1e-24
            ):
                raise ValueError("Freeform edges must not cross or touch")
    signed = sum(a[0] * b[1] - b[0] * a[1] for a, b in edges)
    if abs(signed) <= 1e-12:
        raise ValueError("Freeform contour has zero area")
    if signed < 0:
        points.reverse()
    triangles = []
    while len(points) > 3:
        for i, b in enumerate(points):
            a, c = points[i - 1], points[(i + 1) % len(points)]
            if _cross(a, b, c) <= 1e-12:
                continue
            other = [
                p
                for j, p in enumerate(points)
                if j not in {i, (i - 1) % len(points), (i + 1) % len(points)}
            ]
            if any(
                _cross(a, b, p) >= -1e-12
                and _cross(b, c, p) >= -1e-12
                and _cross(c, a, p) >= -1e-12
                for p in other
            ):
                continue
            triangles.append([a, b, c])
            points.pop(i)
            break
        else:
            raise ValueError("Freeform contour cannot be partitioned without changing geometry")
    if _cross(*points) <= 1e-12:
        raise ValueError("Freeform contour contains a degenerate edge")
    return triangles + [points]


def freeform_parts(element):
    x, y, w, h = element["box"]
    return [[(x + u * w, y + v * h) for u, v in part] for part in triangulate(element["vertices"])]


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
    if element.get("line_cap") == "round":
        # Circumscribed octagons conservatively cover the visible endpoint disks.
        radius = half / math.cos(math.pi / 8)
        for x, y in ((x1, y1), (x2, y2)):
            parts.append(
                [
                    (
                        x + radius * math.cos(math.pi / 8 + k * math.pi / 4),
                        y + radius * math.sin(math.pi / 8 + k * math.pi / 4),
                    )
                    for k in range(8)
                ]
            )
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
