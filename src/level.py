# level.py
import pygame
import os

def create_level():
    platforms = []
    
    # Основная земля — толще
    platforms.append(pygame.Rect(0, 520, 1200, 80))  # высота 80 пикселей
    
    # Крупные платформы — шире и толще
    platforms.append(pygame.Rect(250, 420, 160, 30))
    platforms.append(pygame.Rect(500, 340, 180, 30))
    platforms.append(pygame.Rect(800, 260, 200, 30))
    platforms.append(pygame.Rect(1100, 380, 160, 30))
    
    # Массивные стены — толще и выше
    platforms.append(pygame.Rect(150, 180, 40, 340))   # левая стена: ширина 40
    platforms.append(pygame.Rect(1000, 100, 40, 420))  # правая стена: ширина 40
    
    # Уступы у стен для wall jump
    platforms.append(pygame.Rect(190, 380, 80, 25))    # у левой стены
    platforms.append(pygame.Rect(920, 300, 80, 25))    # у правой стены
    
    # Дополнительные элементы для паркура
    platforms.append(pygame.Rect(380, 280, 100, 25))
    platforms.append(pygame.Rect(680, 200, 100, 25))
    platforms.append(pygame.Rect(450, 150, 120, 25))   # верхняя платформа
    
    return platforms

class Level:
    def __init__(self):
        self.platforms = create_level()
        self.background = None

        # Путь к фону (если есть)
        bg_path = "assets/sprites/backgrounds/bg.png"
        if os.path.exists(bg_path):
            self.background = pygame.image.load(bg_path).convert()
        else:
            # Тёмный фон: глубокий тёмно-синий → чёрный
            self.background = pygame.Surface((800, 600))
            for y in range(600):
                # Градиент от тёмно-синего (#0a0a20) к чёрному (#000000)
                r = int(10 * (1 - y / 600))
                g = int(10 * (1 - y / 600))
                b = int(32 * (1 - y / 600))
                pygame.draw.line(self.background, (r, g, b), (0, y), (800, y))

    def draw(self, screen, camera):
        # Фон с параллаксом
        if self.background:
            bg_x = -camera.x * 0.3
            # Рисуем два фона для бесшовной прокрутки
            screen.blit(self.background, (bg_x % 800 - 800, 0))
            screen.blit(self.background, (bg_x % 800, 0))

        # Платформы — тёмно-серые, почти чёрные
        for plat in self.platforms:
            # Цвет: тёмно-серый с лёгким акцентом
            color = (60, 60, 70)
            rect_on_screen = (
                plat.x - camera.x,
                plat.y - camera.y,
                plat.width,
                plat.height
            )
            pygame.draw.rect(screen, color, rect_on_screen)
            
            # Добавим лёгкий контур для чёткости (опционально)
            pygame.draw.rect(screen, (40, 40, 50), rect_on_screen, 2)