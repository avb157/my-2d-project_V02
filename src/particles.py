# particles.py

import pygame
import random

class Particle:
    def __init__(self, x, y, color, size, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed = speed
        self.lifetime = lifetime  # ms
        self.age = 0
        self.vel_x = random.uniform(-speed, speed)
        self.vel_y = random.uniform(-speed, speed)

    def update(self, dt_ms):
        self.x += self.vel_x * (dt_ms / 16.7)  
        self.y += self.vel_y * (dt_ms / 16.7)
        self.vel_y += 0.1 * (dt_ms / 16.7)  
        self.age += dt_ms
        return self.age > self.lifetime

    def draw(self, surface, camera):
        if self.age <= self.lifetime:
            alpha = max(0, 255 * (1 - self.age / self.lifetime))
            radius = int(self.size * (1 - self.age / self.lifetime))
            pos = (int(self.x - camera.x), int(self.y - camera.y))
            temp_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (*self.color, int(alpha)), (radius, radius), radius)
            surface.blit(temp_surf, (pos[0] - radius, pos[1] - radius))