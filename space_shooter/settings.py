# settings.py — All game constants and configuration

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Shooter"

# Colors
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
RED         = (220,  50,  50)
GREEN       = (50,  200,  80)
BLUE        = (50,  120, 220)
YELLOW      = (255, 220,  50)
ORANGE      = (255, 140,  0)
CYAN        = (0,   220, 255)
PURPLE      = (160,  50, 220)
GREY        = (120, 120, 120)
DARK_GREY   = (40,   40,  40)
LIGHT_GREY  = (180, 180, 180)

# Player
PLAYER_SPEED        = 5
PLAYER_SHOOT_DELAY  = 280       # ms between shots
PLAYER_START_LIVES  = 3
PLAYER_INVINCIBLE_MS = 1500     # brief invincibility after hit
PLAYER_WIDTH        = 48
PLAYER_HEIGHT       = 48

# Bullet
BULLET_SPEED        = 9
BULLET_WIDTH        = 6
BULLET_HEIGHT       = 16

# Enemy
ENEMY_WIDTH         = 44
ENEMY_HEIGHT        = 44
ENEMY_BASE_SPEED    = 2.0
ENEMY_SPEED_MAX     = 6.0
ENEMY_SPEED_STEP    = 0.0003    # added per frame to base speed

# Spawning
SPAWN_INTERVAL_START = 1400     # ms
SPAWN_INTERVAL_MIN   = 350      # ms (fastest spawn rate)
SPAWN_INTERVAL_STEP  = 0.35     # ms reduction per frame

# Score
SCORE_PER_KILL      = 10

# Power-ups
POWERUP_CHANCE      = 0.12      # 12% chance on enemy death
POWERUP_SPEED       = 2.5
POWERUP_DURATION_MS = 6000      # rapid-fire lasts 6 s
POWERUP_SHOOT_DELAY = 100       # shoot delay during rapid-fire

# Stars (background)
NUM_STARS           = 120
STAR_SPEED_MIN      = 0.5
STAR_SPEED_MAX      = 2.5

# Explosion
EXPLOSION_FRAMES    = 8         # number of animation steps
EXPLOSION_DURATION  = 400       # ms total
