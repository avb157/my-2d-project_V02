# main.py
import pygame
from player import Player
from level import Level
from ui.sound import SoundManager  
import sys

LEVEL_DEATH_Y = 700

# UI-КЛАССЫ

class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Start Game", "Settings", "Quit"]
        self.selected = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_font = pygame.font.Font(None, 64)
        title = title_font.render("My Platformer", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (150, 150, 150)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 250 + i * 60))
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
                        return "start"
                    elif self.selected == 1:
                        return "settings"
                    elif self.selected == 2:
                        pygame.quit()
                        sys.exit()
        return None


class PauseMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Resume", "Main Menu", "Quit"]
        self.selected = 0

    def draw(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected else (180, 180, 180)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 220 + i * 50))
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


class HUD:
    def __init__(self, screen, font, player, start_time):
        self.screen = screen
        self.font = font
        self.player = player
        self.start_time = start_time

    def draw(self):
        health_text = self.font.render(f"Health: {self.player.health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

        elapsed_sec = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.font.render(f"Time: {elapsed_sec}s", True, (255, 255, 255))
        self.screen.blit(timer_text, (10, 40))

        hint = self.font.render("Press ESC to pause", True, (200, 200, 200))
        self.screen.blit(hint, (10, self.screen.get_height() - 30))


class DeathScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("You Died!", True, (255, 0, 0))
        restart = self.font.render("Press R to Restart", True, (255, 255, 255))
        menu = self.font.render("Press M for Main Menu", True, (255, 255, 255))

        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 200))
        self.screen.blit(restart, (self.screen.get_width() // 2 - restart.get_width() // 2, 280))
        self.screen.blit(menu, (self.screen.get_width() // 2 - menu.get_width() // 2, 320))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "menu"
        return None


class WinScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("You Win!", True, (255, 215, 0))
        time_text = self.font.render(f"Time: {self.elapsed_time}s", True, (255, 255, 255))
        restart = self.font.render("Press R to Restart", True, (200, 200, 200))
        menu = self.font.render("Press M for Main Menu", True, (200, 200, 200))

        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 200))
        self.screen.blit(time_text, (self.screen.get_width() // 2 - time_text.get_width() // 2, 260))
        self.screen.blit(restart, (self.screen.get_width() // 2 - restart.get_width() // 2, 320))
        self.screen.blit(menu, (self.screen.get_width() // 2 - menu.get_width() // 2, 360))

    def set_time(self, elapsed_time):
        self.elapsed_time = elapsed_time

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_m:
                    return "menu"
        return None


# ОСНОВНЫЕ КЛАССЫ ИГРЫ

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

    def update(self, target):
        self.x = target.x - self.width // 2
        self.y = 0


def reset_game():
    """Создаёт новый уровень и игрока, возвращает их и время начала."""
    level = Level()

    start_platforms = [plat for plat in level.platforms if plat.x < 300 and plat.width > 80]
    if not start_platforms:
        ground_plat = next(plat for plat in level.platforms if plat.y == 580)
    else:
        ground_plat = max(start_platforms, key=lambda p: p.y)

    spawn_x = 100
    spawn_y = ground_plat.y - 28

    player = Player(spawn_x, spawn_y)
    start_time = pygame.time.get_ticks()
    return level, player, start_time


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Platformer Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    sound_manager = SoundManager()

    game_state = "menu"

    level, player, start_time = reset_game()
    camera = Camera(800, 600)

    main_menu = MainMenu(screen, font)
    pause_menu = PauseMenu(screen, font)
    hud = HUD(screen, font, player, start_time)
    death_screen = DeathScreen(screen, font)
    win_screen = WinScreen(screen, font) 

    running = True
    while running:
        dt_ms = clock.tick(60)

        if game_state == "menu":
            action = main_menu.handle_input()
            main_menu.draw()
            if action == "start":
                level, player, start_time = reset_game()
                camera = Camera(800, 600)
                hud = HUD(screen, font, player, start_time)
                win_screen = WinScreen(screen, font)  
                sound_manager.resume_music()
                game_state = "playing"
            elif action == "settings":
                pass

        elif game_state == "playing":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_state = "paused"

            player.update(level.platforms, dt_ms)
            camera.update(player)

            # Проверка смерти
            if player.health <= 0 or player.rect.top > LEVEL_DEATH_Y:
                game_state = "dead"

            # ПРОВЕРКА ПОБЕДЫ (касание финишной зоны)
            if player.hitbox.colliderect(level.finish_zone):
                elapsed_sec = (pygame.time.get_ticks() - start_time) // 1000
                win_screen.set_time(elapsed_sec)
                game_state = "win"

            screen.fill((0, 0, 0))
            level.draw(screen, camera, dt_ms)
            player.draw(screen, camera)
            hud.draw()

        elif game_state == "paused":
            action = pause_menu.handle_input()
            pause_menu.draw()
            if action == "resume":
                game_state = "playing"
            elif action == "menu":
                sound_manager.stop_music()
                game_state = "menu"

        elif game_state == "dead":
            action = death_screen.handle_input()
            death_screen.draw()
            if action == "restart":
                level, player, start_time = reset_game()
                camera = Camera(800, 600)
                hud = HUD(screen, font, player, start_time)
                sound_manager.resume_music()
                game_state = "playing"
            elif action == "menu":
                sound_manager.stop_music()
                game_state = "menu"

        # ПОБЕДА
        elif game_state == "win":
            action = win_screen.handle_input()
            win_screen.draw()
            if action == "restart":
                level, player, start_time = reset_game()
                camera = Camera(800, 600)
                hud = HUD(screen, font, player, start_time)
                sound_manager.resume_music()
                game_state = "playing"
            elif action == "menu":
                sound_manager.stop_music()
                game_state = "menu"

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()