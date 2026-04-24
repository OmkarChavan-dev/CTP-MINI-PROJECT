# 🚀 Space Shooter

A fully-featured 2D space shooter built with Python 3.10+ and Pygame.
No external asset files required — all graphics are generated procedurally.

## Setup

```bash
pip install pygame numpy        # numpy is optional (enables synthesised sounds)
cd space_shooter
python main.py
```

## Controls

| Action | Key |
|--------|-----|
| Move   | WASD or Arrow Keys |
| Shoot  | SPACE |
| Quit   | ESC |
| Restart (Game Over) | R / ENTER / SPACE |

## Features

- Scrolling star field background
- Player ship with full 2D movement
- Shooting cooldown + rapid-fire power-up
- Shield power-up (absorbs one hit wave)
- Sine-wave drifting enemies
- Particle explosion effects
- Synthesised laser & explosion sounds (via numpy)
- Progressive difficulty (spawn rate + enemy speed)
- HUD: score, lives, health bar, active power-ups
- High-score tracking (session)
- Three game states: Start → Playing → Game Over

## Project Structure

```
space_shooter/
├── main.py       – Game class, state machine, main loop
├── settings.py   – All constants / tuning values
├── player.py     – Player sprite (movement, shooting, power-ups)
├── enemy.py      – Enemy sprite (descent, sine drift)
├── bullet.py     – Bullet + PowerUp sprites
└── utils.py      – Procedural art, particles, stars, sounds, HUD helpers
```
