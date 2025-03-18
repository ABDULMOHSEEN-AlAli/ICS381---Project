import pygame
import random
from environment_constants import *
from game_grid import Grid
from snake import Snake
from food import FoodManager
# from ui import UI
# from ai_agent import SimpleAI, AdvancedAI


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

        self.snake1 = Snake(snake1_pos, BLUE, "Abdulmohseen")
        self.snake2 = Snake(snake2_pos, RED, "Mohammed")

        # Initialize food manager
        self.food_manager = FoodManager(self.grid, [self.snake1, self.snake2])

        # Initialize UI
        # self.ui = UI(self.screen) # ToDo: make new UI

        # Game state
        self.game_over = False
        self.winner = None
        self.turn_count = 0

        # AI agents (optional - comment out if using human controls)
        # self.ai1 = SimpleAI(self.snake1, self.snake2, self.grid, self.food_manager) # ToDo AI
        # self.ai2 = SimpleAI(self.snake2, self.snake1, self.grid, self.food_manager)

    def get_random_position(self):
        """Generate a random position on the grid"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def handle_input(self, event):
        # ToDo: get user input while playing
        """Handle user input for snake movement"""
        if self.game_over:
            # Check for restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__init__()  # Reset the game
            return

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
        # self.ai1.make_move() ToDo: make the AI logic
        # self.ai2.make_move()

        # Update snakes
        self.snake1.update_move(snake1_move)
        self.snake2.update_move(snake2_move)

        # Check for collisions and food
        self.check_collisions()
        self.food_manager.check_food_collection()

        # Check win conditions
        if self.snake1.score >= MAX_SCORE:
            self.game_over = True
            self.winner = self.snake1
        elif self.snake2.score >= MAX_SCORE:
            self.game_over = True
            self.winner = self.snake2

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

        # Check if snakes hit spike Traps
        for trap, _ in self.food_manager.spike_trap_items:
            if head1 == trap:
                self.snake1.score = max(0, self.snake1.score - 1)
                isValid = self.snake1.reduce_length()
                if not isValid:
                    self.game_over = True
                    self.winner = self.snake2
                    return
                self.food_manager.spawn_spike_trap(trap)


            if head2 == trap:
                self.snake2.score = max(0, self.snake2.score - 1)
                isValid = self.snake2.reduce_length()
                if not isValid:
                    self.game_over = True
                    self.winner = self.snake1
                    return
                self.food_manager.spawn_spike_trap(trap)


    # def render(self):
    #     """Render the game"""
    #     # Clear the screen
    #     self.screen.fill(BLACK)
    #
    #     # Draw the grid
    #     self.grid.draw(self.screen)
    #
    #     # Draw food and Traps
    #     self.food_manager.draw(self.screen)
    #
    #     # Draw the snakes
    #     self.snake1.draw(self.screen)
    #     self.snake2.draw(self.screen)
    #
    #     # Draw UI elements (score, etc.)
    #     self.ui.draw_scores(self.snake1.score, self.snake2.score)
    #
    #     # Draw game over message if applicable
    #     if self.game_over:
    #         self.ui.draw_game_over(self.winner)
    #
    #     # Update the display
    #     pygame.display.flip()
