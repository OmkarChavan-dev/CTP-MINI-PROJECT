# bullet.py — Bullet and PowerUp sprite classes

import random
import pygame
from settings import *
from utils import make_bullet_surface, make_powerup_surface


class Bullet(pygame.sprite.Sprite):
    """Player projectile — travels upward."""

    _image_cache: pygame.Surface | None = None

    def __init__(self, x: int, y: int):
        super().__init__()
        if Bullet._image_cache is None:
            Bullet._image_cache = make_bullet_surface()
        self.image = Bullet._image_cache
        self.rect  = self.image.get_rect(centerx=x, bottom=y)

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """Dropped by enemies on death; player collects by touching."""

    KINDS = ("rapid", "shield")

    def __init__(self, x: int, y: int):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.image = make_powerup_surface(self.kind)
        self.rect  = self.image.get_rect(center=(x, y))
        self._angle     = 0.0
        self._base_image = self.image.copy()

    def update(self):
        self.rect.y += int(POWERUP_SPEED)
        # Slow spin
        self._angle = (self._angle + 1.5) % 360
        self.image  = pygame.transform.rotate(self._base_image, self._angle)
        self.rect   = self.image.get_rect(center=self.rect.center)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
