# Game settings
TITLE = "Typing Musician"
WIDTH = 1000
HEIGHT = 600
FPS = 60
FONT = 'fonts/font.ttf'

SCORES_FILE = "leaderboard.csv"

# Background Images
MENU_BG = "graphics/Background/city.jpg"
GAME_BG = "graphics/Background/city2.jpg"
OPT_BG = "graphics/Background/city1.jpg"

# Game Images
STRIPE = "graphics/stripe.png"

# Songs paths
PERFECT = 'songs/levels/Perfect.mp3'
DREAMLAND = 'songs/levels/dream-land.mp3'
PIRATE = 'songs/levels/HesPirate.mp3'
ZEN_SONG = 'songs/levels/zen_pirate.wav'

# Sounds paths
ERROR_SOUND = 'sounds/error.mp3'

# Keys properties
KEY_PIXEL_SPEED = 6 # pixels per frame
KEY_SPEED = int(KEY_PIXEL_SPEED * (60/FPS)) # Proper 
DELAY = int(780 / (KEY_SPEED*FPS) * 1000) # Delay in miliseconds

# Fonts
from pygame import font
FONT20 = font.Font(FONT, 20)
FONT30 = font.Font(FONT, 30)
FONT40 = font.Font(FONT, 40)
FONT45 = font.Font(FONT, 45)
FONT60 = font.Font(FONT, 60)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (200, 200, 200)
DARKGRAY = (50, 50, 50)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
LIGHTERBLUE = (51, 207, 255)
PINK = (228, 108, 235)
RED = (166, 15, 15)
LIGHTGREEN = (16, 196, 76)
PURPLE = (165, 81, 196)