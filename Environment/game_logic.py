import pygame
import random
from environment_constants import *
from game_grid import Grid
from snake import Snake
from food import FoodManager
from newUI import UI
from simple_snake_astar import SimpleAI
from snake_local_search import SnakeLocalSearch
import time

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake AI Competition - ICS 381 Project")

        # Initialize game components
        self.grid = Grid()

        # Create snakes with random positions
        snake1_pos = self.get_random_position()
        snake2_pos = self.get_random_position()
        while snake2_pos == snake1_pos:  # Ensure they don't overlap
            snake2_pos = self.get_random_position()

        self.snake1 = Snake(snake1_pos, BLUE, "Blue Snake")
        self.snake2 = Snake(snake2_pos, ORANGE, "Orange Snake")

        # Initialize food manager
        self.food_manager = FoodManager(self.grid, [self.snake1, self.snake2])

        # Initialize UI
        self.ui = UI(self.screen)

        # Game state
        self.game_over = False
        self.winner = None
        self.turn_count = 0

        # AI agents (optional - comment out if using human controls)
        self.ai1 = SimpleAI(self.snake1, self.snake2, self.grid, self.food_manager) # ToDo AI
        self.ai2 = SnakeLocalSearch(self.snake2, self.snake1, self.grid, self.food_manager)

    def get_random_position(self):
        """Generate a random position on the grid"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def handle_input(self, event):
        """Handle user input for snake movement"""
        if self.game_over:
            # Check for restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()  # Reset the game
            return

        # Human controls - only needed if not using AI
        if event.type == pygame.KEYDOWN:
            # Snake 1 controls
            if event.key == pygame.K_UP and self.snake1.direction != DOWN:
                self.snake1.update_move(UP)
            elif event.key == pygame.K_DOWN and self.snake1.direction != UP:
                self.snake1.update_move(DOWN)
            elif event.key == pygame.K_LEFT and self.snake1.direction != RIGHT:
                self.snake1.update_move(LEFT)
            elif event.key == pygame.K_RIGHT and self.snake1.direction != LEFT:
                self.snake1.update_move(RIGHT)

            # Snake 2 controls
            if event.key == pygame.K_w and self.snake2.direction != DOWN:
                self.snake2.update_move(UP)
            elif event.key == pygame.K_s and self.snake2.direction != UP:
                self.snake2.update_move(DOWN)
            elif event.key == pygame.K_a and self.snake2.direction != RIGHT:
                self.snake2.update_move(LEFT)
            elif event.key == pygame.K_d and self.snake2.direction != LEFT:
                self.snake2.update_move(RIGHT)

    def update(self):
        """Update game state"""
        if self.game_over:
            return

        # Increment turn counter
        self.turn_count += 1

        # Check for max turns
        if self.turn_count >= MAX_TURNS:
            self.game_over = True
            if self.snake1.score > self.snake2.score:
                self.winner = self.snake1
            elif self.snake2.score > self.snake1.score:
                self.winner = self.snake2
            else:
                self.winner = None  # Tie
            return

        # Get AI moves
        # calculate the time takes to make disition 
        start_time_1 = time.perf_counter_ns() 
        self.ai1.make_move() 
        end_time_1 = time.perf_counter_ns()
        self.snake1.timer(end_time_1 - start_time_1)
        # print(f"AI 1 decision time: {(end_time_1 - start_time_1)/ 1_000_000} ns")
        
        start_time_2 = time.perf_counter_ns() 
        self.ai2.make_move()
        end_time_2 = time.perf_counter_ns() 
        self.snake2.timer(end_time_2 - start_time_2)    
        # print(f"AI 2 decision time: {(end_time_2 - start_time_2)/ 1_000_000} ns")


        # Check for collisions and food
        self.check_collisions()
        self.food_manager.collect_item()

        # Check win conditions
        if self.snake1.score >= MAX_SCORE:
            self.game_over = True
            self.winner = self.snake1
        elif self.snake2.score >= MAX_SCORE:
            self.game_over = True
            self.winner = self.snake2

        elif self.snake1.score <0:
            self.game_over = True
            self.winner = self.snake2

        elif self.snake2.score < 0:
            self.game_over = True
            self.winner = self.snake1



    def check_collisions(self):
        """Check for collisions between snakes, walls, and themselves"""
        # Check if snakes hit the wall
        if not self.grid.is_valid_position(self.snake1.get_head_position()):
            self.game_over = True
            self.winner = self.snake2
            return

        if not self.grid.is_valid_position(self.snake2.get_head_position()):
            self.game_over = True
            self.winner = self.snake1
            return

        # Check if snakes hit themselves
        if self.snake1.check_self_collision():
            self.game_over = True
            self.winner = self.snake2
            return

        if self.snake2.check_self_collision():
            self.game_over = True
            self.winner = self.snake1
            return

        # Check if snakes hit each other
        head1 = self.snake1.get_head_position()
        head2 = self.snake2.get_head_position()

        # Head-to-head collision (tie)
        if head1 == head2:
            self.game_over = True
            self.winner = None
            return

        # Snake 1 hits Snake 2's body
        for segment in self.snake2.body[1:]:
            if head1 == segment:
                self.game_over = True
                self.winner = self.snake2
                return

        # Snake 2 hits Snake 1's body
        for segment in self.snake1.body[1:]:
            if head2 == segment:
                self.game_over = True
                self.winner = self.snake1
                return


    def render(self):
        """Render the game"""
        # Clear the screen
        self.screen.fill(BLACK)

        # Create grid surface
        grid_surface = pygame.Surface((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        grid_surface.fill(DARK_GREY)  # Changed to dark grey like in the image

        # Draw grid with lines
        self.ui.draw_grid(grid_surface)

        # Draw food and Traps
        self.food_manager.draw(self.screen)

        # Draw the snakes
        self.snake1.draw(self.screen)
        self.snake2.draw(self.screen)

        # Draw UI elements - passing snake lengths
        self.ui.draw_scores(
            self.snake1.score,
            self.snake2.score,
            len(self.snake1.body),
            len(self.snake2.body)
        )

        # Draw game over message if applicable
        if self.game_over:
            self.ui.draw_game_over(self.winner, self.turn_count, self.snake1, self.snake2)

        # Update the display
        pygame.display.flip()