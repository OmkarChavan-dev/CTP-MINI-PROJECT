# utils.py — Helper functions, procedural asset generation, star field

import math
import random
import pygame
from settings import *


# ─────────────────────────────────────────────
#  Procedural asset generation (no image files)
# ─────────────────────────────────────────────

def make_player_surface(w=PLAYER_WIDTH, h=PLAYER_HEIGHT) -> pygame.Surface:
    """Draw a sleek triangular spaceship pointing upward."""
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    # Main body
    body = [
        (w // 2,          2),          # nose
        (w - 4,           h - 6),      # right wing tip
        (w * 3 // 4,      h - 14),     # right inner
        (w // 2,          h - 8),      # tail center
        (w // 4,          h - 14),     # left inner
        (4,               h - 6),      # left wing tip
    ]
    pygame.draw.polygon(surf, CYAN, body)
    pygame.draw.polygon(surf, WHITE, body, 2)
    # Cockpit
    cockpit = [
        (w // 2,  8),
        (w * 3 // 5, h // 2),
        (w // 2,  h // 2 + 4),
        (w * 2 // 5, h // 2),
    ]
    pygame.draw.polygon(surf, BLUE, cockpit)
    # Engine glow
    pygame.draw.ellipse(surf, YELLOW, (w // 2 - 6, h - 10, 12, 8))
    return surf


def make_enemy_surface(w=ENEMY_WIDTH, h=ENEMY_HEIGHT) -> pygame.Surface:
    """Draw a menacing alien ship pointing downward."""
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    body = [
        (w // 2,        h - 2),     # bottom tip
        (w - 4,         6),          # top-right
        (w * 3 // 4,    14),         # right inner
        (w // 2,        8),          # top center
        (w // 4,        14),         # left inner
        (4,             6),           # top-left
    ]
    pygame.draw.polygon(surf, RED, body)
    pygame.draw.polygon(surf, ORANGE, body, 2)
    # Eye
    pygame.draw.ellipse(surf, YELLOW, (w // 2 - 7, h // 3, 14, 10))
    pygame.draw.ellipse(surf, BLACK,  (w // 2 - 3, h // 3 + 2, 6, 6))
    return surf


def make_bullet_surface(w=BULLET_WIDTH, h=BULLET_HEIGHT) -> pygame.Surface:
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, YELLOW, (0, 0, w, h))
    pygame.draw.ellipse(surf, WHITE,  (1, 1, w - 2, 4))
    return surf


def make_powerup_surface(kind: str, size=28) -> pygame.Surface:
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    color = YELLOW if kind == "rapid" else GREEN
    pygame.draw.circle(surf, color, (size // 2, size // 2), size // 2)
    pygame.draw.circle(surf, WHITE,  (size // 2, size // 2), size // 2, 2)
    font = pygame.font.SysFont("arial", 14, bold=True)
    label = "R" if kind == "rapid" else "S"
    txt = font.render(label, True, BLACK)
    surf.blit(txt, txt.get_rect(center=(size // 2, size // 2)))
    return surf


# ─────────────────────────────────────────────
#  Explosion particle system
# ─────────────────────────────────────────────

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "size")

    def __init__(self, x, y):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 5.5)
        self.x, self.y = float(x), float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.max_life = random.randint(18, 36)
        self.life = self.max_life
        self.color = random.choice([ORANGE, YELLOW, RED, WHITE])
        self.size = random.randint(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12   # slight gravity
        self.life -= 1
        self.size = max(1, self.size - 0.08)

    def draw(self, surface):
        alpha = int(255 * self.life / self.max_life)
        r, g, b = self.color
        color = (min(r, 255), min(g, 255), min(b, 255), alpha)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (self.size, self.size), self.size)
        surface.blit(s, (int(self.x) - self.size, int(self.y) - self.size))

    @property
    def dead(self):
        return self.life <= 0


class ParticleManager:
    def __init__(self):
        self._particles: list[Particle] = []

    def explode(self, x, y, count=22):
        for _ in range(count):
            self._particles.append(Particle(x, y))

    def update(self):
        self._particles = [p for p in self._particles if not p.dead]
        for p in self._particles:
            p.update()

    def draw(self, surface):
        for p in self._particles:
            p.draw(surface)

    def clear(self):
        self._particles.clear()


# ─────────────────────────────────────────────
#  Scrolling star field
# ─────────────────────────────────────────────

class StarField:
    def __init__(self):
        self.stars = []
        for _ in range(NUM_STARS):
            self.stars.append(self._new_star(random.randint(0, SCREEN_HEIGHT)))

    def _new_star(self, y=0):
        x     = random.randint(0, SCREEN_WIDTH)
        speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
        size  = 1 if speed < 1.2 else (2 if speed < 2.0 else 3)
        bright = int(80 + speed / STAR_SPEED_MAX * 175)
        return [x, y, speed, size, bright]

    def update(self):
        for s in self.stars:
            s[1] += s[2]
            if s[1] > SCREEN_HEIGHT:
                s[:] = self._new_star(0)

    def draw(self, surface):
        for x, y, _, size, bright in self.stars:
            c = (bright, bright, bright)
            if size == 1:
                surface.set_at((int(x), int(y)), c)
            else:
                pygame.draw.circle(surface, c, (int(x), int(y)), size)


# ─────────────────────────────────────────────
#  Sound stub (no external files required)
# ─────────────────────────────────────────────

def _synth_shoot() -> pygame.mixer.Sound | None:
    """Generate a short laser blip programmatically."""
    try:
        import numpy as np
        rate = 44100
        dur  = 0.08
        t    = np.linspace(0, dur, int(rate * dur), endpoint=False)
        freq = np.linspace(900, 300, len(t))
        wave = (np.sin(2 * np.pi * freq * t) * 22000).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(0.25)
        return snd
    except Exception:
        return None


def _synth_explosion() -> pygame.mixer.Sound | None:
    try:
        import numpy as np
        rate = 44100
        dur  = 0.25
        t    = np.linspace(0, dur, int(rate * dur), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t))
        env   = np.exp(-t * 14)
        wave  = (noise * env * 28000).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(0.35)
        return snd
    except Exception:
        return None


def _synth_powerup() -> pygame.mixer.Sound | None:
    try:
        import numpy as np
        rate = 44100
        dur  = 0.3
        t    = np.linspace(0, dur, int(rate * dur), endpoint=False)
        freq = np.linspace(400, 1200, len(t))
        wave = (np.sin(2 * np.pi * freq * t) * 20000).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        snd = pygame.sndarray.make_sound(stereo)
        snd.set_volume(0.30)
        return snd
    except Exception:
        return None


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.shoot    = None
        self.boom     = None
        self.powerup  = None
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.shoot   = _synth_shoot()
            self.boom    = _synth_explosion()
            self.powerup = _synth_powerup()
            self.enabled = True
        except Exception:
            pass

    def play_shoot(self):
        if self.shoot:
            self.shoot.play()

    def play_boom(self):
        if self.boom:
            self.boom.play()

    def play_powerup(self):
        if self.powerup:
            self.powerup.play()


# ─────────────────────────────────────────────
#  Font helpers
# ─────────────────────────────────────────────

def render_text(font, text, color, shadow=True, shadow_color=(0, 0, 0)):
    surf = font.render(text, True, color)
    if shadow:
        sh   = font.render(text, True, shadow_color)
        out  = pygame.Surface((surf.get_width() + 2, surf.get_height() + 2), pygame.SRCALPHA)
        out.blit(sh, (2, 2))
        out.blit(surf, (0, 0))
        return out
    return surf


def draw_health_bar(surface, x, y, current, maximum, w=120, h=14):
    ratio = max(0, current / maximum)
    bg_rect  = pygame.Rect(x, y, w, h)
    bar_rect = pygame.Rect(x, y, int(w * ratio), h)
    color = GREEN if ratio > 0.5 else YELLOW if ratio > 0.25 else RED
    pygame.draw.rect(surface, DARK_GREY, bg_rect, border_radius=6)
    if bar_rect.width > 0:
        pygame.draw.rect(surface, color, bar_rect, border_radius=6)
    pygame.draw.rect(surface, GREY, bg_rect, 2, border_radius=6)
