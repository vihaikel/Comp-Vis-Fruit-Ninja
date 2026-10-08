import math

def line_intersects_circle(p1, p2, circle_pos, radius):
    """Mengecek apakah garis tebasan memotong area buah"""
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = circle_pos

    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(cx - x1, cy - y1) <= radius

    t = max(0, min(1, ((cx - x1) * dx + (cy -y1) * dy) / (dx * dx + dy * dy)))
    nearest_x = x1 + t * dx
    nearest_y = y1 + t * dy

    return math.hypot(cx - nearest_x, cy - nearest_y) <= radius