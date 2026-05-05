# 🚀 Space Shooter — CTP Mini Project

A fully-featured 2D space shooter game built from scratch using **Python** and **Pygame**. No external asset files required — all graphics are drawn procedurally with code. Supports power-ups, particle explosions, scrolling star fields, and progressive difficulty scaling.

## ✨ Features

| Feature | Details |
|---|---|
| 🎨 Procedural Graphics | All ships, bullets, and UI drawn with Pygame — no image files needed |
| 🌟 Scrolling Star Field | Parallax star background with 120 stars at varying speeds |
| 👾 Progressive Enemies | Sine-wave drifting enemies that get faster and spawn more frequently |
| 💥 Particle Explosions | 22-particle burst system with physics and fade-out |
| 🔊 Synthesised Sounds | Laser and explosion sounds generated via NumPy — no audio files |
| ⚡ Power-Ups | Rapid Fire (R) and Shield (S) collectibles dropped randomly on kill |
| 🛡️ Shield System | Absorbs damage for 6 seconds with glowing cyan ring indicator |
| 💊 Health + Lives | Health bar with 3 lives; temporary invincibility after taking damage |
| 🏆 High Score | Session-based high score tracking across restarts |
| 🎮 3 Game States | Start screen → Gameplay → Game Over with restart support |

---

## 🗂️ Project Structure

```
space_shooter/
│
├── main.py         # Game class, state machine, main loop & collision handling
├── settings.py     # All constants — speeds, colors, timings, difficulty params
├── player.py       # Player sprite: movement, shooting, invincibility, power-ups
├── enemy.py        # Enemy sprite: sine-wave drift, speed scaling
├── bullet.py       # Bullet + PowerUp sprites (spinning collectibles)
├── utils.py        # Procedural art, particle system, stars, sounds, HUD helpers
└── README.md       # This file
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/OmkarChavan-dev/CTP-MINI-PROJECT.git
cd CTP-MINI-PROJECT

# 2. Create a virtual environment (recommended)
python -m venv .venv

# 3. Activate it
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install pygame numpy

# 5. Run the game
python main.py
```

> **Note:** `numpy` is optional but enables synthesised laser and explosion sounds.

---

## 🕹️ Controls

| Action | Key |
|---|---|
| Move Ship | `W A S D` or `↑ ← ↓ →` Arrow Keys |
| Shoot | `SPACE` |
| Restart (Game Over screen) | `R` / `ENTER` / `SPACE` |
| Quit | `ESC` |

---

## 🎯 How to Play

1. **Press any key** on the start screen to begin
2. **Shoot enemies** with `SPACE` — each kill earns **10 points**
3. **Collect power-ups** dropped by enemies:
   - 🟡 **R (Rapid Fire)** — triples your fire rate for 6 seconds
   - 🟢 **S (Shield)** — protects from damage for 6 seconds
4. **Avoid enemies** hitting you or passing through the bottom of the screen
5. Lose all **3 lives** and it's game over — beat your high score!

---

## 📈 Difficulty Scaling

The game continuously increases in difficulty:

- **Spawn rate** starts at 1.4 seconds and ramps down to a minimum of 0.35 seconds
- **Enemy speed** increases gradually from 2.0 up to a cap of 6.0
- **Level indicator** in the top-right shows your current difficulty level (1–10)

---

## 🧱 Architecture Overview

```
main.py (Game)
├── State Machine: start → playing → gameover
├── Sprite Groups: all_sprites, enemies, bullets, powerups
└── Systems:
    ├── StarField         (utils.py) — scrolling background
    ├── ParticleManager   (utils.py) — explosion effects
    └── SoundManager      (utils.py) — synthesised audio

Player (player.py)
├── Movement (WASD / Arrow)
├── Shooting with cooldown
├── Invincibility frames after damage
└── Power-up timers (rapid fire, shield)

Enemy (enemy.py)
└── Sine-wave lateral drift + downward movement

Bullet / PowerUp (bullet.py)
├── Bullet travels upward and despawns off-screen
└── PowerUp spins and falls downward
```

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Game Framework:** [Pygame 2.6](https://www.pygame.org/)
- **Audio Synthesis:** [NumPy](https://numpy.org/) (optional)
- **Design Pattern:** Object-Oriented Programming (OOP) with Pygame sprite system

---

## 📋 Requirements

```
pygame>=2.0.0
numpy>=1.20.0   # optional, for sound effects
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 👨‍💻 Author

**Omkar Chavan**  
GitHub: [@OmkarChavan-dev](https://github.com/OmkarChavan-dev)

**Shrutika Bhand**
Github: [@shrutikabhand](https://github.com/shrutikabhand)

---

## 📄 License

This project is licensed under the MIT License.
