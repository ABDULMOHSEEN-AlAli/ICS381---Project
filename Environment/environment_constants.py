# Game dimensions
GRID_SIZE = 20  # 20x20 grid 
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
VISIBILITY_RANGE = 2  # How far snakes can see other snakes
EXPANSION_RATE_NORMAL = 1
EXPANSION_RATE_SUPER = 1
MAX_SCORE = 50  # Game ends when a snake reaches this score
MAX_TURNS = 500  # Maximum number of turns before the game ends

# Item probabilities
NORMAL_FOOD_PROB = 0.8  # 80% chance for normal food
SUPER_FOOD_PROB = 0.2   # 20% chance for super food
FOOD_AMOUNT = 4
SPIKE_TRAPS_AMOUNT = 40  # Number of spike traps to be placed on the grid


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Items rewards
NORMAL_FOOD_REWARD = 100
SUPER_FOOD_REWARD = 130

SPIKE_TRAP_COST = 300  # Penalty for hitting a spike trap
SAVE_MOVE_COST = 80  # Reward for saving a move
NORMAL_FOOD_COST = 40
SUPER_FOOD_COST = 20
