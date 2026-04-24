# enemy.py — Enemy sprite with sine-wave lateral drift

import math
import random
import pygame
from settings import *
from utils import make_enemy_surface


class Enemy(pygame.sprite.Sprite):
    """Alien enemy that descends with slight horizontal drift."""

    _image_cache: pygame.Surface | None = None

    def __init__(self, speed: float = ENEMY_BASE_SPEED):
        super().__init__()
        if Enemy._image_cache is None:
            Enemy._image_cache = make_enemy_surface()
        self.image  = Enemy._image_cache
        self.rect   = self.image.get_rect(
            centerx=random.randint(ENEMY_WIDTH // 2, SCREEN_WIDTH - ENEMY_WIDTH // 2),
            bottom=0,
        )
        self.speed       = speed
        self._phase      = random.uniform(0, math.tau)   # sine phase offset
        self._amplitude  = random.uniform(0.6, 1.8)      # horizontal swing
        self._tick       = 0

    def update(self):
        self._tick += 1
        self.rect.y += self.speed
        # Gentle sine drift
        dx = math.sin(self._phase + self._tick * 0.04) * self._amplitude
        self.rect.x = int(self.rect.x + dx)
        # Keep on screen horizontally
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        # Remove if past bottom
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
