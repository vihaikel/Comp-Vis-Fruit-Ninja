import math
import numpy as np
import pygame

def make_levelup_sound():
    """Membuat suara arpeggio naik (C-E-G-C) tanpa file audio. None jika audio tidak tersedia."""
    mixer = pygame.mixer.get_init()
    if mixer is None:
        return None
    freq, _, channels = mixer

    notes = [(523.25, 0.08), (659.25, 0.08), (783.99, 0.08), (1046.50, 0.35)]
    parts = []
    for hz, dur in notes:
        t = np.arange(int(freq * dur)) / freq
        parts.append(np.sin(2 * np.pi * hz * t) * np.exp(-t * 6))  # nada meluruh pelan

    samples = (np.concatenate(parts) * 0.4 * 32767).astype(np.int16)
    if channels > 1:
        samples = np.ascontiguousarray(np.repeat(samples[:, None], channels, axis=1))
    return pygame.sndarray.make_sound(samples)

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