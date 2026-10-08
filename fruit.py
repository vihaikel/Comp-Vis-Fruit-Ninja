import random
import pygame
import config

class Fruit:
    def __init__(self, level=1):
        self.radius = config.FRUIT_RADIUS
        self.x = random.randint(100, config.WIDTH - 100)
        self.y = config.HEIGHT + self.radius

        # Kecepatan lontar bertambah sesuai level
        speed_bonus = (level - 1) * 1.5
        self.vx = random.randint(int(-4 - speed_bonus), int(4 + speed_bonus))
        self.vy = random.randint(int(-18 - speed_bonus), int(-14 - speed_bonus))
        self.gravity = config.GRAVITY
        self.color = (random.randint(100, 255), random.randint(50, 200), random.randint(0, 100)) # Warna buah acak
        self.sliced = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity

    def draw(self, surface):
        if not self.sliced:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius, 2)  # Outline putih