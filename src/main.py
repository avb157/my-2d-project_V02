# main.py
import pygame
from player import Player
from level import Level

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        self.x = target.x - self.width // 2
        self.y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Создаём уровень
    level = Level()

    # === ОПРЕДЕЛЯЕМ ТОЧКУ СПАВНА ===
    min_x = min(plat.x for plat in level.platforms)
    max_x = max(plat.x + plat.width for plat in level.platforms)
    spawn_x = (min_x + max_x) // 2  # центр уровня

    # Предположим, что основная земля на y=520, а hitbox.height=28
    spawn_y = 520 - 28  # чтобы стоял на земле

    player = Player(spawn_x, spawn_y)
    camera = Camera(800, 600)

    running = True
    while running:
        dt_ms = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(level.platforms, dt_ms)
        camera.update(player)

        screen.fill((0, 0, 0))  # фон будет перекрыт уровнем
        level.draw(screen, camera)
        player.draw(screen, camera)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()