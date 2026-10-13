import numpy as np

# Pengaturan untuk ukuran layar
WIDTH = 800
HEIGHT = 600
FPS = 30

# Pengaturan Computer Vision (CV) (HSV Color Range)
# Default: Hijau Terang
LOWER_COLOR = np.array([35, 100, 100])  # Batas bawah warna hijau dalam format HSV
UPPER_COLOR = np.array([85, 255, 255])  # Batas atas warna hijau dalam format HSV

MIN_CONTOUR_AREA = 400
MAX_TRAIL_LEN = 8

# Mekanik Game
TIME_PER_LEVEL = 30  # Waktu per level dalam detik
SPAWN_INTERVAL = 10  # Interval waktu untuk spawn buah (dalam milidetik)
POINTS_PER_LEVEL = 150
FRUIT_RADIUS = 35
GRAVITY = 0.6