# player.py
import pygame
import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.vel_x = 0
        self.vel_y = 0
        
        # Физика движения
        self.acceleration = 0.6
        self.friction = 0.85
        self.max_speed = 7
        self.gravity = 0.8
        self.jump_power = -15
        self.jump_held = False
        self.jump_start_time = 0
        self.max_jump_hold_time = 0.3  # секунды

        # Состояния
        self.on_ground = False
        self.on_wall = False
        self.wall_side = 0  # -1 — слева, 1 — справа

        # Двойной прыжок
        self.jump_count = 0
        self.max_jumps = 2

        # Перекат (dash)
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 8
        self.dash_speed = 12

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        # === Горизонтальное движение с ускорением и трением ===
        if not self.is_dashing:
            target_vel_x = 0
            if keys[pygame.K_LEFT]:
                target_vel_x = -self.max_speed
            if keys[pygame.K_RIGHT]:
                target_vel_x = self.max_speed

            # Плавное ускорение
            self.vel_x += (target_vel_x - self.vel_x) * self.acceleration
        else:
            # При перекате скорость фиксирована
            pass

        # === Прыжок: обычный, двойной, плавный ===
        if keys[pygame.K_SPACE]:
            if not self.jump_held:
                # Начало прыжка
                if self.on_ground:
                    self.jump_count = 1
                    self.vel_y = self.jump_power
                    self.on_ground = False
                    self.jump_held = True
                    self.jump_start_time = time.time()
                elif self.jump_count < self.max_jumps:
                    self.jump_count += 1
                    self.vel_y = self.jump_power * 0.9
                    self.jump_held = True
                    self.jump_start_time = time.time()
        else:
            # Отпускание кнопки — обрезаем прыжок
            if self.jump_held and self.vel_y < 0:
                current_time = time.time()
                held_time = current_time - self.jump_start_time
                if held_time < self.max_jump_hold_time:
                    # Уменьшаем силу прыжка пропорционально времени удержания
                    self.vel_y *= held_time / self.max_jump_hold_time
            self.jump_held = False

        # === Перекат (Dash) ===
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if keys[pygame.K_LSHIFT] and self.dash_cooldown == 0 and not self.is_dashing:
            direction = 1
            if self.vel_x < 0:
                direction = -1
            elif self.vel_x == 0:
                # Если стоит на месте — используем последнее направление взгляда
                direction = 1 if not hasattr(self, 'last_dir') or self.last_dir >= 0 else -1
            self.vel_x = direction * self.dash_speed
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 60  # ~1 сек при 60 FPS

        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                # После переката применяем трение
                self.vel_x *= 0.7

        # === Гравитация ===
        if not self.is_dashing:
            self.vel_y += self.gravity

        # Ограничение скорости падения
        if self.vel_y > 12:
            self.vel_y = 12

        # === Обновление позиции по X ===
        self.x += self.vel_x
        self.rect.x = int(self.x)
        self.check_collisions(platforms, 'horizontal')

        # === Обновление позиции по Y ===
        self.y += self.vel_y
        self.rect.y = int(self.y)
        self.check_collisions(platforms, 'vertical')

        # === Обнаружение стены для лазания ===
        self.on_wall = False
        self.wall_side = 0
        if not self.on_ground:
            if self.check_wall_collision(-1, platforms):
                self.on_wall = True
                self.wall_side = -1
            elif self.check_wall_collision(1, platforms):
                self.on_wall = True
                self.wall_side = 1

        # === Лазание по стене ===
        if self.on_wall:
            if keys[pygame.K_UP]:
                self.vel_y = -2  # медленное движение вверх
            elif keys[pygame.K_DOWN]:
                self.vel_y = 2   # медленное движение вниз
            else:
                self.vel_y = max(self.vel_y, 0)  # не падаем мгновенно, но не поднимаемся

        # === Wall Jump ===
        if keys[pygame.K_SPACE] and self.on_wall and not self.jump_held:
            self.vel_y = self.jump_power * 0.8
            self.vel_x = -self.wall_side * 8  # отталкивание от стены
            self.on_wall = False
            self.wall_side = 0
            self.jump_held = True
            self.jump_start_time = time.time()
            self.jump_count = 1  # считаем как один прыжок

        # Сохраняем направление для dash
        if self.vel_x > 0:
            self.last_dir = 1
        elif self.vel_x < 0:
            self.last_dir = -1

    def check_wall_collision(self, side, platforms):
    # Проверяет наличие стены СНАРУЖИ игрока в указанном направлении.
    # side: -1 — слева, 1 — справа
        if side == -1:
            # Проверяем точку СЛЕВА от игрока
            test_x = self.rect.left - 1
        elif side == 1:
            # Проверяем точку СПРАВА от игрока
            test_x = self.rect.right + 1
        else:
            return False

        test_rect = pygame.Rect(test_x, self.rect.top, 1, self.rect.height)
        for plat in platforms:
            if test_rect.colliderect(plat):
                return True
        return False

    def check_collisions(self, platforms, direction):
        for plat in platforms:
            if self.rect.colliderect(plat):
                if direction == 'horizontal':
                    if self.vel_x > 0:  # движение вправо
                        self.rect.right = plat.left
                    elif self.vel_x < 0:  # движение влево
                        self.rect.left = plat.right
                    self.x = self.rect.x
                    self.vel_x = 0  # останавливаем горизонтальную скорость при столкновении
                elif direction == 'vertical':
                    if self.vel_y > 0:  # падение
                        self.rect.bottom = plat.top
                        self.on_ground = True
                        self.jump_count = 0  # сброс счётчика прыжков
                    elif self.vel_y < 0:  # прыжок вверх
                        self.rect.top = plat.bottom
                    self.vel_y = 0
                    self.y = self.rect.y

    def draw(self, screen, camera):
        color = (0, 255, 0)
        if self.is_dashing:
            color = (255, 255, 0)  # жёлтый при перекате
        elif self.on_wall:
            color = (0, 100, 255)  # синий при лазании
        pygame.draw.rect(
            screen,
            color,
            (self.x - camera.x, self.y - camera.y, self.width, self.height)
        )