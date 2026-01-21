# animation.py

import pygame
import os

class Animation:
    def __init__(self, frames, frame_duration=100, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.last_update = 0
        self.finished = False

    def update(self, dt_ms):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True

    def get_current_frame(self):
        return self.frames[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.finished = False