import pygame
import sys

class DeathScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("You Died! Press R to restart or ESC to quit.", True, (255, 255, 255))
        rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
        return None