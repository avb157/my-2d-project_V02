# player.py
import pygame
import time
import os
import random
from animation import Animation
from particles import Particle
from typing import List

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        
        # Физика
        self.acceleration = 0.6
        self.friction = 0.85
        self.max_speed = 7
        self.gravity = 0.8
        self.jump_power = -15
        self.jump_held = False
        self.jump_start_time = 0
        self.max_jump_hold_time = 0.3

        self.on_ground = False
        self.on_wall = False
        self.wall_side = 0

        self.jump_count = 0
        self.max_jumps = 2

        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_duration = 8
        self.dash_speed = 12

        # Анимации
        self.animations = {}
        self.load_animations()
        self.current_animation = self.animations['idle']
        self.facing_right = True
        self.image = self.current_animation.get_current_frame()

        # Частицы
        self.particles = []

        # Для определения состояния
        self.state = 'idle'

        self.health = 100 

        # ХИТБОКС — для коллизий
        self.hitbox_size = (32, 32)  
        self.hitbox = pygame.Rect(x, y, *self.hitbox_size)
        self.rect = self.hitbox 

    def load_animations(self):
        """Загружает анимации из папок. Если папок нет — создаёт цветные заглушки."""
        sprite_dir = "assets/sprites/player/"
        states = ['idle', 'run', 'jump', 'fall', 'wall_slide', 'roll', 'climb']

        for state in states:
            path = os.path.join(sprite_dir, state)
            frames = []
            if os.path.exists(path):
                for file in sorted(os.listdir(path)):
                    if file.endswith('.png'):
                        img = pygame.image.load(os.path.join(path, file)).convert_alpha()
                        # Масштабируем до 32x32, если нужно
                        if img.get_size() != (32, 32):
                            img = pygame.transform.scale(img, (32, 32))
                        frames.append(img)
        
            # Если нет спрайтов — создаём цветной прямоугольник как заглушку
            if not frames:
                color_map = {
                    'idle': (0, 255, 0),
                    'run': (0, 200, 0),
                    'jump': (255, 255, 0),
                    'fall': (255, 165, 0),
                    'wall_slide': (0, 100, 255),
                    'roll': (255, 0, 255),
                    'climb': (100, 100, 255)
                }
                color = color_map.get(state, (255, 255, 255))
                surf = pygame.Surface((32, 32), pygame.SRCALPHA)
                pygame.draw.rect(surf, color, (0, 0, 32, 32))
                frames = [surf]

            # УСТАНАВЛИВАЕМ 12 КАДРОВ В СЕКУНДУ
            duration = 200  
            loop = True

            if state == 'idle':
                duration = 250 
            elif state == 'run':
                duration = 167 
            elif state == 'jump' or state == 'roll':
                duration = 250  
                loop = False
            elif state == 'fall':
                duration = 200  
            elif state == 'wall_slide' or state == 'climb':
                duration = 250  

            self.animations[state] = Animation(frames, duration, loop)

    def determine_state(self):
        if self.on_wall:
            if abs(self.vel_y) > 0.1:
                return 'climb'
            else:
                return 'wall_slide'
        elif self.is_dashing:
            return 'roll'
        elif self.vel_y < 0:
            return 'jump'
        elif self.vel_y > 0.1:
            return 'fall'
        elif abs(self.vel_x) > 0.5:
            return 'run'
        else:
            return 'idle'

    def add_dust_particles(self):
        if random.random() < 0.3: 
            for _ in range(3):
                p = Particle(
                    x=self.rect.centerx,
                    y=self.rect.bottom,
                    color=(180, 180, 180),
                    size=2,
                    speed=1.5,
                    lifetime=400
                )
                self.particles.append(p)

    def add_spark_particles(self):
        for _ in range(6):
            p = Particle(
                x=self.rect.centerx,
                y=self.rect.centery,
                color=(255, 215, 0),
                size=1.5,
                speed=2.5,
                lifetime=300
            )
            self.particles.append(p)

    def update(self, platforms: List[pygame.Rect], dt_ms: int):
        # Сохраняем предыдущее состояние для сравнения
        prev_state = self.state
        prev_on_ground = self.on_ground
        prev_on_wall = self.on_wall
        prev_is_dashing = self.is_dashing

        keys = pygame.key.get_pressed()

        if not self.is_dashing:
            target_vel_x = 0
            if keys[pygame.K_LEFT]:
                target_vel_x = -self.max_speed
            if keys[pygame.K_RIGHT]:
                target_vel_x = self.max_speed
            self.vel_x += (target_vel_x - self.vel_x) * self.acceleration
        else:
            pass

        if keys[pygame.K_SPACE]:
            if not self.jump_held:
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
            if self.jump_held and self.vel_y < 0:
                current_time = time.time()
                held_time = current_time - self.jump_start_time
                if held_time < self.max_jump_hold_time:
                    self.vel_y *= held_time / self.max_jump_hold_time
            self.jump_held = False

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        if keys[pygame.K_LSHIFT] and self.dash_cooldown == 0 and not self.is_dashing:
            direction = 1
            if self.vel_x < 0:
                direction = -1
            elif self.vel_x == 0:
                direction = 1 if not hasattr(self, 'last_dir') or self.last_dir >= 0 else -1
            self.vel_x = direction * self.dash_speed
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown = 60

        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vel_x *= 0.7

        if not self.is_dashing:
            self.vel_y += self.gravity
        if self.vel_y > 12:
            self.vel_y = 12

        # Горизонтальное движение
        self.hitbox.centerx = int(self.x + self.vel_x)
        self.check_collisions(platforms, 'horizontal')
        self.x = self.hitbox.centerx

        # Вертикальное движение
        self.hitbox.centery = int(self.y + self.vel_y)
        self.check_collisions(platforms, 'vertical')
        self.y = self.hitbox.centery

        # Обновляем rect (для отрисовки и частиц)
        self.rect = self.hitbox

        # Обнаружение стены
        self.on_wall = False
        self.wall_side = 0
        if not self.on_ground:
            if self.check_wall_collision(-1, platforms):
                self.on_wall = True
                self.wall_side = -1
            elif self.check_wall_collision(1, platforms):
                self.on_wall = True
                self.wall_side = 1

        if self.on_wall:
            if keys[pygame.K_UP]:
                self.vel_y = -2
            elif keys[pygame.K_DOWN]:
                self.vel_y = 2
            else:
                self.vel_y = max(self.vel_y, 0)

        if keys[pygame.K_SPACE] and self.on_wall and not self.jump_held:
            self.vel_y = self.jump_power * 0.8
            self.vel_x = -self.wall_side * 8
            self.on_wall = False
            self.wall_side = 0
            self.jump_held = True
            self.jump_start_time = time.time()
            self.jump_count = 1
            self.add_spark_particles()

        if self.vel_x > 0:
            self.last_dir = 1
            self.facing_right = True
        elif self.vel_x < 0:
            self.last_dir = -1
            self.facing_right = False

        # ОБНОВЛЕНИЕ АНИМАЦИИ
        self.state = self.determine_state()

        if self.state != prev_state:
            self.current_animation = self.animations[self.state]
            self.current_animation.reset()

        self.current_animation.update(dt_ms)
        self.image = self.current_animation.get_current_frame()

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Частицы
        if self.state == 'run' and self.on_ground and prev_on_ground:
            self.add_dust_particles()

        self.particles = [p for p in self.particles if not p.update(dt_ms)]

    def check_wall_collision(self, side: int, platforms: List[pygame.Rect]) -> bool:
        if side == -1:
            test_x = self.hitbox.left - 1
        elif side == 1:
            test_x = self.hitbox.right + 1
        else:
            return False
        test_rect = pygame.Rect(test_x, self.hitbox.top, 1, self.hitbox.height)
        for plat in platforms:
            if test_rect.colliderect(plat):
                return True
        return False

    def check_collisions(self, platforms: List[pygame.Rect], direction: str):
        for plat in platforms:
            if self.hitbox.colliderect(plat):
                if direction == 'horizontal':
                    if self.vel_x > 0:
                        self.hitbox.right = plat.left
                    elif self.vel_x < 0:
                        self.hitbox.left = plat.right
                    self.x = self.hitbox.centerx
                    self.vel_x = 0
                elif direction == 'vertical':
                    if self.vel_y > 0:
                        self.hitbox.bottom = plat.top
                        self.on_ground = True
                        self.jump_count = 0
                    elif self.vel_y < 0:
                        self.hitbox.top = plat.bottom
                    self.vel_y = 0
                    self.y = self.hitbox.centery

    def draw(self, screen, camera):
        screen.blit(self.image, (self.hitbox.x - camera.x, self.hitbox.y - camera.y))
        for p in self.particles:
            p.draw(screen, camera)