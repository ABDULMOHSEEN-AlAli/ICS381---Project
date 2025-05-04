# Snake AI Competition

This project is a Snake game with AI competition where two snake agents compete against each other using different algorithms (A* Search and Local Search). The game includes normal food, super food, and spike traps in a 20x20 grid environment.

## Project Structure

- `Environment/` - Contains all the game files
  - `environment_constants.py` - Game constants and settings
  - `game_grid.py` - Grid implementation
  - `snake.py` - Snake class implementation
  - `food.py` - Food manager for different items
  - `newUI.py` - UI implementation
  - `game_logic.py` - Main game logic
  - `snake_astar.py` - A* Search algorithm implementation
  - `snake_local_search.py` - Local Search algorithm implementation
  - `main.py` - Entry point for the game

## Requirements

- Python 3.6+
- Pygame

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ICS381-Project.git
cd ICS381-Project
```

2. Install the required dependencies:
```bash
pip install pygame
```

## Running the Game

To run the game, execute the main.py file:
```bash
python Environment/main.py
```

## Game Controls

The game is designed to run with AI agents, but if you want to control the snakes manually, you can modify the game_logic.py file and use the following controls:

- Blue Snake:
  - Up: Arrow Up
  - Down: Arrow Down
  - Left: Arrow Left
  - Right: Arrow Right

- Orange Snake:
  - Up: W
  - Down: S
  - Left: A
  - Right: D

## Game Rules

- The game is played on a 20x20 grid.
- Blue Snake uses A* Search algorithm.
- Orange Snake uses Local Search algorithm.
- Each snake can see other snakes within a visibility range of 2 cells.
- Normal food increases score by 1.
- Super food increases score by 1-3 (random).
- Spike traps reduce snake length and decrease score by 1.
- The game ends when:
  - A snake collides with a wall
  - A snake collides with itself
  - A snake collides with the other snake
  - A snake reaches the maximum score (20)
  - Maximum turns (500) are reached

## Performance Statistics

At the end of the game, performance statistics are displayed:
- Total turns
- Time taken by each AI agent (in milliseconds)
- Final scores

## Customization

You can customize game settings by modifying the constants in `environment_constants.py`:
- Grid size and cell dimensions
- Food and trap probabilities
- Visibility range
- Maximum score and turns
- Rewards and penalties