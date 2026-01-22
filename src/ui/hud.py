import pygame

class HUD:
    def __init__(self, screen, font, player):
        self.screen = screen
        self.font = font
        self.player = player

    def draw(self):
        # Здоровье
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

        # Таймер (если есть)
        timer_text = self.font.render(f"Time: {int(pygame.time.get_ticks()/1000)}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 50))

        # Подсказки (например, "Press SPACE to jump")
        hint_text = self.font.render("Press ESC to pause", True, (200, 200, 200))
        self.screen.blit(hint_text, (10, self.screen.get_height() - 40))