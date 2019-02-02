TITLE = "Half Life 3"
WIDTH = 1000
HEIGHT = 600
FPS = 70
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 15

# Starting platforms
STD_HEIGHT = 20
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (200, 430, 600, 20),
                 (125, 300, 100, STD_HEIGHT),
                 (350, 200, 100, STD_HEIGHT),
                 (175, 100, 50, STD_HEIGHT)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
