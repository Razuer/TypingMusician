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
DREAMLAND = 'songs/mp3/dream-land.mp3'
PIRATE = 'songs/levels/HesPirate.mp3'

# Keys properties
KEY_PIXEL_SPEED = 6 # pixels per frame
KEY_SPEED = int(KEY_PIXEL_SPEED * (60/FPS)) # Proper 
DELAY = int(780 / (KEY_SPEED*FPS) * 1000) # Delay in miliseconds

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (200, 200, 200)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
PINK = (228, 108, 235)