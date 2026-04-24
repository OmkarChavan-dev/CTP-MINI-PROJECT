# player.py — Player sprite with movement, shooting, and power-up handling

import pygame
from settings import *
from utils import make_player_surface
from bullet import Bullet


class Player(pygame.sprite.Sprite):
    """The player-controlled ship."""

    MAX_HEALTH = 100

    def __init__(self, bullet_group: pygame.sprite.Group, sound_mgr):
        super().__init__()
        self._base_image = make_player_surface()
        self.image       = self._base_image.copy()
        self.rect        = self.image.get_rect(
            centerx=SCREEN_WIDTH // 2,
            bottom=SCREEN_HEIGHT - 20,
        )
        self.bullet_group  = bullet_group
        self.sound         = sound_mgr

        # Stats
        self.health        = self.MAX_HEALTH
        self.lives         = PLAYER_START_LIVES
        self.score         = 0

        # Shooting
        self._last_shot    = 0
        self._shoot_delay  = PLAYER_SHOOT_DELAY

        # Invincibility after hit
        self._invincible   = False
        self._inv_timer    = 0
        self._blink        = False

        # Power-up state
        self._rapid_timer  = 0
        self.shield_active = False
        self._shield_timer = 0

    # ── Public helpers ─────────────────────────────────────────────────────

    @property
    def alive_ok(self) -> bool:
        return self.lives > 0

    def apply_powerup(self, kind: str):
        if kind == "rapid":
            self._shoot_delay = POWERUP_SHOOT_DELAY
            self._rapid_timer = POWERUP_DURATION_MS
        elif kind == "shield":
            self.shield_active = True
            self._shield_timer = POWERUP_DURATION_MS

    def take_damage(self, amount: int = 34):
        if self._invincible or self.shield_active:
            return
        self.health -= amount
        if self.health <= 0:
            self.lives -= 1
            self.health = self.MAX_HEALTH if self.lives > 0 else 0
            self._start_invincibility()

    def _start_invincibility(self):
        self._invincible = True
        self._inv_timer  = PLAYER_INVINCIBLE_MS

    # ── Pygame sprite interface ────────────────────────────────────────────

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        self._handle_movement(keys)
        self._handle_shooting(keys, now)
        self._tick_timers(now)
        self._update_image()

    def _handle_movement(self, keys):
        dx = dy = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += PLAYER_SPEED
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= PLAYER_SPEED
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += PLAYER_SPEED
        self.rect.x = max(0,                  min(SCREEN_WIDTH  - self.rect.width,  self.rect.x + dx))
        self.rect.y = max(0,                  min(SCREEN_HEIGHT - self.rect.height, self.rect.y + dy))

    def _handle_shooting(self, keys, now: int):
        if keys[pygame.K_SPACE] and now - self._last_shot >= self._shoot_delay:
            b = Bullet(self.rect.centerx, self.rect.top)
            self.bullet_group.add(b)
            self._last_shot = now
            self.sound.play_shoot()

    def _tick_timers(self, now: int):
        dt = pygame.time.Clock().tick(0)   # just get delta via stored approach

        # Invincibility
        if self._invincible:
            self._inv_timer -= 16           # approx 60 fps → ~16 ms/frame
            self._blink = (self._inv_timer // 80) % 2 == 0
            if self._inv_timer <= 0:
                self._invincible = False
                self._blink      = False

        # Rapid fire
        if self._rapid_timer > 0:
            self._rapid_timer -= 16
            if self._rapid_timer <= 0:
                self._shoot_delay = PLAYER_SHOOT_DELAY

        # Shield
        if self._shield_timer > 0:
            self._shield_timer -= 16
            if self._shield_timer <= 0:
                self.shield_active = False

    def _update_image(self):
        if self._blink:
            # Semi-transparent during invincibility blink
            self.image = self._base_image.copy()
            self.image.set_alpha(80)
        else:
            self.image = self._base_image.copy()
            self.image.set_alpha(255)

    def draw_extras(self, surface: pygame.Surface):
        """Draw shield ring if active."""
        if self.shield_active:
            alpha = 160
            r     = max(self.rect.width, self.rect.height) // 2 + 6
            s     = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*CYAN, alpha), (r + 2, r + 2), r, 3)
            surface.blit(s, (self.rect.centerx - r - 2, self.rect.centery - r - 2))
