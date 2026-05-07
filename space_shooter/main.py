#!/usr/bin/env python3
"""
main.py — Space Shooter
Entry point: initialises pygame, owns the state machine and main loop.

States
------
  "start"    — title / instructions screen
  "playing"  — active gameplay
  "gameover" — game-over overlay with restart option
"""

import sys
import random
import pygame

# ── Boot pygame and detect fullscreen resolution BEFORE importing any local
#    module, so every "from settings import *" sees the real screen size. ──
pygame.init()
_screen_probe = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
_SW, _SH = _screen_probe.get_size()
pygame.display.quit()   # will be re-created properly below

import settings as _settings
_settings.SCREEN_WIDTH  = _SW
_settings.SCREEN_HEIGHT = _SH

# Now import everything else — they will read the patched values
from settings import *
from utils    import StarField, ParticleManager, SoundManager, render_text, draw_health_bar
from player   import Player
from enemy    import Enemy
from bullet   import Bullet, PowerUp


# ─────────────────────────────────────────────────────────────
#  Game class
# ─────────────────────────────────────────────────────────────

class Game:
    def __init__(self):
        pygame.init()
        self.screen  = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock   = pygame.time.Clock()

        # Fonts
        self.font_xl  = pygame.font.SysFont("arial", 64, bold=True)
        self.font_lg  = pygame.font.SysFont("arial", 36, bold=True)
        self.font_md  = pygame.font.SysFont("arial", 22, bold=True)
        self.font_sm  = pygame.font.SysFont("arial", 16)

        # Shared systems
        self.stars    = StarField()
        self.particles= ParticleManager()
        self.sound    = SoundManager()

        self.state    = "start"
        self.high_score = 0
        self._init_gameplay()

    # ── Initialise / reset gameplay objects ───────────────────────────────

    def _init_gameplay(self):
        # Sprite groups
        self.bullets  = pygame.sprite.Group()
        self.enemies  = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Player
        self.player   = Player(self.bullets, self.sound)
        self.all_sprites.add(self.player)

        # Difficulty state
        self._spawn_timer    = 0
        self._spawn_interval = SPAWN_INTERVAL_START   # ms, shrinks over time
        self._enemy_speed    = ENEMY_BASE_SPEED
        self._frame          = 0
        self._last_time      = pygame.time.get_ticks()

        self.particles.clear()

    # ── Main loop ─────────────────────────────────────────────────────────

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            self._handle_events()
            if self.state == "start":
                self._update_start()
                self._draw_start()
            elif self.state == "playing":
                self._update_playing(dt)
                self._draw_playing()
            elif self.state == "gameover":
                self._update_gameover()
                self._draw_gameover()
            pygame.display.flip()

    # ── Event handling ────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if self.state == "start":
                    self.state = "playing"
                elif self.state == "gameover":
                    if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                        self._init_gameplay()
                        self.state = "playing"

    # ── START screen ──────────────────────────────────────────────────────

    def _update_start(self):
        self.stars.update()

    def _draw_start(self):
        self.screen.fill(BLACK)
        self.stars.draw(self.screen)

        title = render_text(self.font_xl, "SPACE SHOOTER", CYAN)
        sub   = render_text(self.font_lg, "Press any key to begin", WHITE)
        hint  = render_text(self.font_sm, "WASD / Arrow Keys  ·  SPACE to shoot  ·  ESC to quit", GREY)
        hs    = render_text(self.font_md, f"High Score: {self.high_score}", YELLOW)

        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 180)))
        self.screen.blit(sub,   sub.get_rect(center=(SCREEN_WIDTH // 2, 280)))
        self.screen.blit(hint,  hint.get_rect(center=(SCREEN_WIDTH // 2, 340)))
        self.screen.blit(hs,    hs.get_rect(center=(SCREEN_WIDTH // 2, 400)))

        controls = [
            ("Move",  "WASD / Arrow Keys"),
            ("Shoot", "SPACE"),
            ("Quit",  "ESC"),
        ]
        panel_y = 450
        for action, key in controls:
            a = self.font_sm.render(f"{action}:", True, LIGHT_GREY)
            k = self.font_sm.render(key,          True, CYAN)
            self.screen.blit(a, (SCREEN_WIDTH // 2 - 100, panel_y))
            self.screen.blit(k, (SCREEN_WIDTH // 2,       panel_y))
            panel_y += 26

    # ── PLAYING update ────────────────────────────────────────────────────

    def _update_playing(self, dt: int):
        self._frame += 1
        now = pygame.time.get_ticks()

        # Difficulty ramp
        self._spawn_interval = max(
            SPAWN_INTERVAL_MIN,
            self._spawn_interval - SPAWN_INTERVAL_STEP
        )
        self._enemy_speed = min(ENEMY_SPEED_MAX, ENEMY_BASE_SPEED + self._frame * ENEMY_SPEED_STEP)

        # Spawn enemies
        self._spawn_timer += dt
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_timer = 0
            e = Enemy(speed=self._enemy_speed)
            self.enemies.add(e)
            self.all_sprites.add(e)

        # Update all sprites
        self.all_sprites.update()
        self.bullets.update()
        self.powerups.update()
        self.stars.update()
        self.particles.update()

        # ── Collisions: bullets vs enemies ────────────────────────────────
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for enemy, _ in hits.items():
            cx, cy = enemy.rect.center
            self.particles.explode(cx, cy)
            self.sound.play_boom()
            self.player.score += SCORE_PER_KILL

            if random.random() < POWERUP_CHANCE:
                pu = PowerUp(cx, cy)
                self.powerups.add(pu)
                self.all_sprites.add(pu)

        # ── Collisions: enemies vs player ─────────────────────────────────
        if not self.player._invincible:
            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, True)
            for e in enemy_hits:
                self.particles.explode(*e.rect.center, count=15)
                self.player.take_damage(34)
                if not self.player.alive_ok:
                    self._end_game()
                    return

        # ── Collisions: power-ups vs player ───────────────────────────────
        pu_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pu in pu_hits:
            self.player.apply_powerup(pu.kind)
            self.sound.play_powerup()

        # ── Check enemies reaching bottom ─────────────────────────────────
        for e in list(self.enemies):
            if e.rect.top > SCREEN_HEIGHT and e.alive():
                e.kill()
                self.player.take_damage(20)
                if not self.player.alive_ok:
                    self._end_game()
                    return

    def _end_game(self):
        self.high_score = max(self.high_score, self.player.score)
        self.state = "gameover"

    # ── PLAYING draw ──────────────────────────────────────────────────────

    def _draw_playing(self):
        self.screen.fill(BLACK)
        self.stars.draw(self.screen)

        self.powerups.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.bullets.draw(self.screen)
        self.particles.draw(self.screen)
        self.player.draw_extras(self.screen)

        # ── HUD ───────────────────────────────────────────────────────────
        p = self.player

        score_surf = render_text(self.font_md, f"Score: {p.score}", WHITE)
        self.screen.blit(score_surf, (10, 10))

        lives_surf = render_text(self.font_md, f"Lives: {'♥ ' * p.lives}", RED)
        self.screen.blit(lives_surf, (10, 36))

        hp_label = render_text(self.font_sm, "HP", GREY, shadow=False)
        self.screen.blit(hp_label, (10, 64))
        draw_health_bar(self.screen, 36, 65, p.health, Player.MAX_HEALTH)

        hud_y = 84
        if p.shield_active:
            s = render_text(self.font_sm, "⚡ SHIELD", CYAN)
            self.screen.blit(s, (10, hud_y)); hud_y += 20
        if p._rapid_timer > 0:
            s = render_text(self.font_sm, "⚡ RAPID FIRE", YELLOW)
            self.screen.blit(s, (10, hud_y))

        hs = render_text(self.font_md, f"Best: {self.high_score}", GREY)
        self.screen.blit(hs, (SCREEN_WIDTH - hs.get_width() - 10, 10))

        level = int((SPAWN_INTERVAL_START - self._spawn_interval) /
                    (SPAWN_INTERVAL_START - SPAWN_INTERVAL_MIN) * 10) + 1
        lvl = render_text(self.font_sm, f"Level {level}", GREY)
        self.screen.blit(lvl, (SCREEN_WIDTH - lvl.get_width() - 10, 36))

    # ── GAME OVER screen ──────────────────────────────────────────────────

    def _update_gameover(self):
        self.stars.update()
        self.particles.update()

    def _draw_gameover(self):
        self.screen.fill(BLACK)
        self.stars.draw(self.screen)
        self.particles.draw(self.screen)

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        go   = render_text(self.font_xl, "GAME OVER", RED)
        sc   = render_text(self.font_lg, f"Score: {self.player.score}", WHITE)
        hs   = render_text(self.font_lg, f"High Score: {self.high_score}", YELLOW)
        rest = render_text(self.font_md, "Press R / ENTER / SPACE to restart", CYAN)
        quit_= render_text(self.font_sm, "ESC to quit", GREY)

        cx = SCREEN_WIDTH // 2
        self.screen.blit(go,   go.get_rect(center=(cx, 180)))
        self.screen.blit(sc,   sc.get_rect(center=(cx, 270)))
        self.screen.blit(hs,   hs.get_rect(center=(cx, 320)))
        self.screen.blit(rest, rest.get_rect(center=(cx, 400)))
        self.screen.blit(quit_,quit_.get_rect(center=(cx, 440)))


# ─────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    game = Game()
    game.run()
