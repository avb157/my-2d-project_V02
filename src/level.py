# level.py
import pygame
import os
import random
import math

def create_level():
    platforms = []
    
    # ЛЕВАЯ НЕПРОХОДИМАЯ СТЕНА: от пола до потолка + козырёк 
    platforms.append(pygame.Rect(0, 0, 60, 600))        
    platforms.append(pygame.Rect(0, 0, 400, 60))        
    
    # ОСНОВНАЯ ЗЕМЛЯ (длинная)
    platforms.append(pygame.Rect(0, 580, 3500, 40))    
    
    # СЕКЦИЯ 1: Начало — первые платформы и дыра
    platforms.append(pygame.Rect(200, 500, 100, 25))
    platforms.append(pygame.Rect(400, 500, 100, 25))    
    platforms.append(pygame.Rect(600, 440, 90, 25))
    
    # СЕКЦИЯ 2: Вертикальный паркур (стены + уступы) 
    platforms.append(pygame.Rect(800, 150, 40, 430))    
    platforms.append(pygame.Rect(950, 150, 40, 430))    
    # Уступы для wall jump
    platforms.append(pygame.Rect(840, 500, 110, 20))
    platforms.append(pygame.Rect(840, 420, 110, 20))
    platforms.append(pygame.Rect(840, 340, 110, 20))
    platforms.append(pygame.Rect(840, 260, 110, 20))
    platforms.append(pygame.Rect(840, 180, 110, 20))
    
    # СЕКЦИЯ 3: Длинная пропасть с островками
    platforms.append(pygame.Rect(1150, 480, 70, 25))
    platforms.append(pygame.Rect(1350, 420, 70, 25))
    platforms.append(pygame.Rect(1550, 360, 70, 25))
    platforms.append(pygame.Rect(1750, 300, 70, 25))
    
    # СЕКЦИЯ 4: Высокие башни и финал
    platforms.append(pygame.Rect(2000, 250, 60, 330))
    platforms.append(pygame.Rect(2250, 200, 60, 380))
    platforms.append(pygame.Rect(2500, 150, 150, 30))
    
    # СЕКЦИЯ 5: Финальные препятствия
    platforms.append(pygame.Rect(2800, 400, 80, 25))
    platforms.append(pygame.Rect(3000, 340, 80, 25))
    platforms.append(pygame.Rect(3200, 280, 80, 25))
    platforms.append(pygame.Rect(3400, 220, 100, 30))  
    
    # Мелкие платформы для точных прыжков
    platforms.append(pygame.Rect(1050, 520, 60, 20))
    platforms.append(pygame.Rect(1900, 520, 60, 20))
    platforms.append(pygame.Rect(2700, 520, 60, 20))
    
    return platforms

    platforms.append(("finish", pygame.Rect(3420, 200, 60, 80))) 

class Level:
    def __init__(self):
        self.platforms = create_level()
        self.finish_zone = pygame.Rect(3420, 200, 60, 80)
        self.time = 0.0
        
        # Неоновые огни
        self.neon_lights = []
        for _ in range(70):  # больше огней на длинном уровне
            x = random.randint(0, 3500)
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

        # Фон (тёмное небо)
        bg_surface = pygame.Surface((width, height))
        for y in range(height):
            t = y / height
            r = int(5 * (1 - t))
            g = int(5 * (1 - t))
            b = int(20 + 10 * (1 - t))
            pygame.draw.line(bg_surface, (r, g, b), (0, y), (width, y))
        
        bg_x = -camera.x * 0.1
        screen.blit(bg_surface, (bg_x % width - width, 0))
        screen.blit(bg_surface, (bg_x % width, 0))

        # Неоновые огни
        for x, y, base_color, freq in self.neon_lights:
            pulse = math.sin(self.time * freq) * 0.5 + 0.5
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
                glow = pygame.Surface((12, 12), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*color, 80), (6, 6), 6)
                screen.blit(glow, (int(screen_x) - 6, int(screen_y) - 6))

        # Городские здания 
        building_colors = [(20, 20, 35), (25, 25, 40)]
        buildings = [
            (-300, 400, 200, 200),
            (3600, 300, 250, 300),
            (300, 520, 120, 80),
            (700, 500, 100, 100),
            (1200, 480, 130, 120),
            (1800, 450, 140, 150),
            (2400, 420, 160, 180),
            (3000, 400, 180, 200),
        ]
        for bx, by, bw, bh in buildings:
            screen_x = bx - camera.x * 0.3
            if -bw < screen_x < width:
                color = random.choice(building_colors)
                pygame.draw.rect(screen, color, (screen_x, by, bw, bh))

        # Платформы
        for plat in self.platforms:
            rect_on_screen = (
                plat.x - camera.x,
                plat.y - camera.y,
                plat.width,
                plat.height
            )
            pygame.draw.rect(screen, (35, 35, 50), rect_on_screen)
            edge_color = random.choice([(80, 40, 120), (40, 100, 150), (120, 60, 80)])
            pygame.draw.rect(screen, edge_color, rect_on_screen, 2)

        # ФИНИШНАЯ ЗОНА
        finish_on_screen = (
            self.finish_zone.x - camera.x,
            self.finish_zone.y - camera.y,
            self.finish_zone.width,
            self.finish_zone.height
        )
        pygame.draw.rect(screen, (255, 215, 0), finish_on_screen)  # золотой цвет
        pygame.draw.rect(screen, (255, 255, 255), finish_on_screen, 2)  # белая рамка