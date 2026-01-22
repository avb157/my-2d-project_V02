# level.py
import pygame
import os
import random
import math

def create_level():
    platforms = []
    
    # Основная земля — крыши зданий
    platforms.append(pygame.Rect(0, 540, 1600, 60))
    
    # Здания и балконы
    platforms.append(pygame.Rect(200, 460, 180, 30))   # балкон
    platforms.append(pygame.Rect(500, 400, 200, 30))
    platforms.append(pygame.Rect(850, 340, 220, 30))
    platforms.append(pygame.Rect(1200, 420, 180, 30))
    
    # Высокие здания (стены)
    platforms.append(pygame.Rect(150, 200, 50, 340))    # левая башня
    platforms.append(pygame.Rect(1400, 150, 50, 390))   # правая башня
    
    # Уступы для wall jump
    platforms.append(pygame.Rect(200, 400, 70, 25))
    platforms.append(pygame.Rect(1330, 360, 70, 25))
    
    # Дополнительные элементы
    platforms.append(pygame.Rect(380, 320, 100, 25))
    platforms.append(pygame.Rect(700, 260, 120, 25))
    platforms.append(pygame.Rect(1000, 280, 100, 25))
    
    return platforms

class Level:
    def __init__(self):
        self.platforms = create_level()
        self.time = 0.0
        
        # Неоновые огни (x, y, цвет, яркость, частота мерцания)
        self.neon_lights = []
        for _ in range(30):
            x = random.randint(0, 1600)
            y = random.randint(100, 500)
            color = random.choice([
                (255, 50, 100),   # розовый
                (50, 200, 255),   # голубой
                (255, 200, 50),   # жёлтый
                (100, 50, 255)    # фиолетовый
            ])
            freq = random.uniform(0.5, 2.0)
            self.neon_lights.append((x, y, color, freq))

    def update(self, dt_ms):
        self.time += dt_ms / 1000.0

    def draw(self, screen, camera, dt_ms):
        self.update(dt_ms)
        width, height = screen.get_size()

        # === Фон: тёмное небо ===
        bg_surface = pygame.Surface((width, height))
        
        # Градиент: от чёрного (внизу) к тёмно-синему (вверху)
        for y in range(height):
            t = y / height
            r = int(5 * (1 - t))
            g = int(5 * (1 - t))
            b = int(20 + 10 * (1 - t))
            pygame.draw.line(bg_surface, (r, g, b), (0, y), (width, y))
        
        # Параллакс фона
        bg_x = -camera.x * 0.1
        screen.blit(bg_surface, (bg_x % width - width, 0))
        screen.blit(bg_surface, (bg_x % width, 0))

        # === Мерцающие неоновые огни ===
        for x, y, base_color, freq in self.neon_lights:
            # Пульсация яркости
            pulse = math.sin(self.time * freq) * 0.5 + 0.5  # от 0 до 1
            brightness = 0.6 + 0.4 * pulse
            color = (
                min(255, int(base_color[0] * brightness)),
                min(255, int(base_color[1] * brightness)),
                min(255, int(base_color[2] * brightness))
            )
            screen_x = x - camera.x
            screen_y = y - camera.y
            if -10 < screen_x < width + 10 and -10 < screen_y < height + 10:
                pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), 3)
                # Свечение (soft glow)
                glow = pygame.Surface((12, 12), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*color, 80), (6, 6), 6)
                screen.blit(glow, (int(screen_x) - 6, int(screen_y) - 6))

        # === Городские здания (силуэты) ===
        # Рисуем тёмные прямоугольники как здания на заднем плане
        building_colors = [(20, 20, 35), (25, 25, 40)]
        buildings = [
            (-100, 400, 100, 200),
            (1700, 380, 120, 220),
            (300, 480, 80, 120),
            (600, 450, 90, 150),
            (1000, 470, 100, 130),
        ]
        for bx, by, bw, bh in buildings:
            screen_x = bx - camera.x * 0.3  # параллакс
            if -bw < screen_x < width:
                color = random.choice(building_colors)
                pygame.draw.rect(screen, color, (screen_x, by, bw, bh))

        # === Платформы (крыши, балконы) ===
        for plat in self.platforms:
            rect_on_screen = (
                plat.x - camera.x,
                plat.y - camera.y,
                plat.width,
                plat.height
            )
            # Тёмно-серый с неоновой кромкой
            pygame.draw.rect(screen, (35, 35, 50), rect_on_screen)
            # Неоновая подсветка (случайный цвет)
            edge_color = random.choice([(80, 40, 120), (40, 100, 150), (120, 60, 80)])
            pygame.draw.rect(screen, edge_color, rect_on_screen, 2)