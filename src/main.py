# main.py
import pygame
from player import Player
from level import create_level
from camera import Camera

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")
clock = pygame.time.Clock()

# Создание объектов
player = Player(100, 300)
platforms = create_level()
camera = Camera(WIDTH, HEIGHT)

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    player.update(platforms)
    camera.update(player)

    # Отрисовка
    screen.fill((0, 0, 0))  # чёрный фон

    # Отрисовка платформ с учётом камеры
    for plat in platforms:
        pygame.draw.rect(screen, (150, 150, 150), (plat.x - camera.x, plat.y - camera.y, plat.width, plat.height))

    player.draw(screen, camera)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()