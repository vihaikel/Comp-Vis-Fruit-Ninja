import sys
import cv2
import pygame
import numpy as np
import config

from cv_tracker import ColorTracker
from fruit import Fruit
from utils import line_intersects_circle

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Fruit Ninja - Computer Vision")
    clock = pygame.time.Clock()

    font_ui = pygame.font.SysFont("Arial", 28, bold=True)
    font_pause = pygame.font.SysFont("Arial", 60, bold=True)
    font_sub = pygame.font.SysFont("Arial", 2)

    tracker = ColorTracker(camera_index=0)

    fruits = []
    score = 0
    spawn_timer = 0
    is_paused = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    is_paused = not is_paused

        frame, current_pos = tracker.process_frame()
        if frame is None:
            break
        
        # Kalkulasi level dan frekuensi kemunculan buah
        level = (score // config.POINTS_PER_LEVEL) + 1
        spawn_interval = max(12, config.SPAWN_INTERVAL - (level - 1) * 4)

        # Pembaruan Logika Game Hanya akan berjalan jika game tidak dipause
        if not is_paused:
            spawn_timer += 1
            if spawn_timer > spawn_interval:
                fruits.append(Fruit(level=level))
                spawn_timer = 0
            
            for fruit in fruits[:]:
                fruit.update()

                if not fruit.sliced and len(tracker.trail_points) >= 2:
                    p1 = tracker.trail_points[-2]
                    p2 = tracker.trail_points[-1]
                    if line_intersects_circle(p1, p2, (fruit.x, fruit.y), fruit.radius):
                        fruit.sliced = True
                        score += 10

                if fruit.y - fruit.radius > config.HEIGHT + 50 or fruit.sliced:
                    score  -= 5 if not fruit.sliced else 0
                    fruits.remove(fruit)

        # Render Frame Kamera
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.image.frombuffer(frame_rgb.tobytes(), (config.WIDTH, config.HEIGHT), "RGB")
        screen.blit(frame_surface, (0, 0))

        # Render Buah
        for fruit in fruits:
            fruit.draw(screen)

        # Render Garis Tebasan
        if len(tracker.trail_points) > 1:
            for i in range(1, len(tracker.trail_points)):
                thickness = int(np.sqrt(config.MAX_TRAIL_LEN / float(i + 1)) * 5)
                pygame.draw.line(screen, (0, 255, 255), tracker.trail_points[i - 1], tracker.trail_points[i], thickness)

        if current_pos:
            pygame.draw.circle(screen, (255, 255, 0), current_pos, 8)

        # Render UI Skor
        score_text = font_ui.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font_ui.render(f"Level: {level}", True, (255, 215,0))
        screen.blit(score_text, (20, 20))
        screen.blit(level_text, (20, 55))

        if is_paused:
            overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            pause_surface = font_pause.render("PAUSED", True, (255, 255, 255))
            sub_surface = font_sub.render("Tekan SPASI untuk Melanjutkan", True, (200, 200,200))

            pause_rect = pause_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 - 20))
            sub_rect = sub_surface.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 30))

            screen.blit(pause_surface, pause_rect)
            screen.blit(sub_surface, sub_rect)
            
        pygame.display.flip()
        clock.tick(config.FPS)

    tracker.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()