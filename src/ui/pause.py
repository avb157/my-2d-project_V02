import pygame
import sys

class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Resume", "Main Menu", "Quit"]
        self.selected = 0

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width()//2, 200 + i*60))
            self.screen.blit(text, rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.selected == 0:
                        return "resume"
                    elif self.selected == 1:
                        return "menu"
                    elif self.selected == 2:
                        pygame.quit()
                        sys.exit()
        return None