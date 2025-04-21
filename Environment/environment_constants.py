# Game dimensions
# from food import FoodManager

GRID_SIZE = 20  # 20x20 grid as specified in the proposal
CELL_SIZE = 35  # Size of each cell in pixels
GRID_WIDTH = GRID_SIZE
GRID_HEIGHT = GRID_SIZE
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 80


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (50, 50, 50)
BLUE = (0, 128, 255)  # Snake 1 color
ORANGE = (255, 128, 0)   # Snake 2 color
DARK_GREY = (175, 175, 175)


# Game settings
SNAKE_SPEED = 15  # Updates per second
INITIAL_SNAKE_LENGTH = 1
VISIBILITY_RANGE = 2  # How far snakes can see other snakes
EXPANSION_RATE_NORMAL = 1
EXPANSION_RATE_SUPER = 1
MAX_SCORE = 20  # Game ends when a snake reaches this score
MAX_TURNS = 90999999999999  # Maximum number of turns before the game ends

# Item probabilities
NORMAL_FOOD_PROB = 0.8  # 80% chance for normal food
SUPER_FOOD_PROB = 0.2   # 20% chance for super food
FOOD_AMOUNT = 4
SPIKE_TRAPS_AMOUNT = 2


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
