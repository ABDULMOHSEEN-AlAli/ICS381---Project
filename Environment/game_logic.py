import pygame
import random
from environment_constants import *
from game_grid import Grid
from snake import Snake
from food import FoodManager
from newUI import UI
from snake_astar import SnakeAI
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

        # AI agents
        self.ai1 = SnakeAI(self.snake1, self.snake2, self.grid, self.food_manager) 
        self.ai2 = SnakeLocalSearch(self.snake2, self.snake1, self.grid, self.food_manager)
        
        # Visualization flags
        self.show_paths = False        # Show A* planned path
        self.show_all_paths = False    # Show all explored paths
        self.show_heatmap = False      # Show local search heatmap
        self.show_considered = False   # Show nodes considered by A*
        self.show_help = False         # Show keyboard help

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

        # Visualization control
        if event.type == pygame.KEYDOWN:
            # Toggle A* path visualization
            if event.key == pygame.K_v:
                self.show_paths = not self.show_paths
                
            # Toggle all explored paths
            elif event.key == pygame.K_a:
                self.show_all_paths = not self.show_all_paths
                
            # Toggle local search heatmap
            elif event.key == pygame.K_h:
                self.show_heatmap = not self.show_heatmap
                
            # Toggle nodes considered by A*
            elif event.key == pygame.K_c:
                self.show_considered = not self.show_considered
                
            # Toggle help display
            elif event.key == pygame.K_F1:
                self.show_help = not self.show_help
                
            # Pause gameplay (for analysis)
            elif event.key == pygame.K_p:
                self.paused = not getattr(self, 'paused', False)
        
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
            
        # Skip update if paused
        if getattr(self, 'paused', False):
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
        
        # calculate the time takes to make decision 
        start_time_1 = time.perf_counter_ns() 
        self.ai1.make_move() 
        end_time_1 = time.perf_counter_ns()
        self.snake1.timer(end_time_1 - start_time_1)
        
        start_time_2 = time.perf_counter_ns() 
        self.ai2.make_move()
        end_time_2 = time.perf_counter_ns() 
        self.snake2.timer(end_time_2 - start_time_2)    

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
        elif self.snake1.score < 0:
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
        
        # Draw visualization elements if enabled
        self._draw_visualizations()

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
        
        # Draw help if enabled
        if self.show_help:
            self._draw_help()
            
        # Draw paused indicator
        if getattr(self, 'paused', False):
            self._draw_paused()

        # Draw game over message if applicable
        if self.game_over:
            self.ui.draw_game_over(self.winner, self.turn_count, self.snake1, self.snake2)

        # Update the display
        pygame.display.flip()
        
    def _draw_visualizations(self):
        """Draw visualization elements if enabled"""
        # Draw nodes considered by A*
        if self.show_considered and hasattr(self.ai1, 'considered_nodes'):
            nodes = self.ai1.considered_nodes
            if nodes:
                # Get min and max values for normalization
                scores = list(nodes.values())
                min_score = min(scores)
                max_score = max(scores)
                score_range = max_score - min_score if max_score > min_score else 1
                
                # Draw each considered node with color based on score
                for pos, score in nodes.items():
                    # Skip positions with snakes
                    if pos in self.snake1.body or pos in self.snake2.body:
                        continue
                        
                    # Normalize score (0 to 1)
                    norm_score = (score - min_score) / score_range
                    
                    # Use purple gradient (darker = higher score)
                    color = (
                        int(100 + 155 * norm_score),  # Red component
                        20,                           # Green component
                        int(255 - 155 * norm_score),  # Blue component
                        80                            # Alpha
                    )
                    
                    cell_rect = pygame.Rect(
                        pos[0] * CELL_SIZE, 
                        pos[1] * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    cell_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    cell_surface.fill(color)
                    self.screen.blit(cell_surface, cell_rect)
        
        # Draw all explored paths
        if self.show_all_paths and hasattr(self.ai1, 'all_explored_paths'):
            paths = self.ai1.all_explored_paths
            if paths:
                # First draw all explored (non-chosen) paths in gray
                for path_type, path in paths:
                    if path_type == 'explored':
                        self._draw_path(path, (150, 150, 150, 100))  # Gray with alpha
        
        # Draw A* path (chosen path)
        if self.show_paths and hasattr(self.ai1, 'current_path'):
            path = self.ai1.current_path
            if path:
                self._draw_path(path, (0, 150, 255, 150))  # Blue with alpha
                
                # Draw target indicator
                if hasattr(self.ai1, 'current_target') and self.ai1.current_target:
                    target = self.ai1.current_target
                    target_rect = pygame.Rect(
                        target[0] * CELL_SIZE,
                        target[1] * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, (0, 255, 255), target_rect, 3)  # Cyan border for target
        
        # Draw local search heatmap
        if self.show_heatmap and hasattr(self.ai2, 'evaluated_cells'):
            cells = self.ai2.evaluated_cells
            if cells:
                # Get min and max values for normalization
                scores = list(cells.values())
                min_score = min(scores)
                max_score = max(scores)
                score_range = max_score - min_score if max_score > min_score else 1
                
                # Draw each evaluated cell with color based on score
                for pos, score in cells.items():
                    # Normalize score (0 to 1)
                    norm_score = (score - min_score) / score_range
                    
                    # Create color gradient (red for high cost, green for low)
                    color = (
                        int(255 * norm_score),         # Red component 
                        int(255 * (1 - norm_score)),   # Green component
                        0,                             # Blue component
                        150                            # Alpha
                    )
                    
                    cell_rect = pygame.Rect(
                        pos[0] * CELL_SIZE,
                        pos[1] * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    cell_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    cell_surface.fill(color)
                    self.screen.blit(cell_surface, cell_rect)
                
                # Highlight best move if available
                if hasattr(self.ai2, 'best_move') and self.ai2.best_move:
                    best_pos = self.ai2.best_move
                    best_rect = pygame.Rect(
                        best_pos[0] * CELL_SIZE,
                        best_pos[1] * CELL_SIZE,
                        CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, (255, 255, 0, 200), best_rect, 3)
        
        # Draw visualization legend if any visualization is enabled
        if self.show_paths or self.show_heatmap or self.show_considered or self.show_all_paths:
            # Draw legend
            legend_rect = pygame.Rect(10, 10, 290, 100)  # Made taller for additional entry
            legend_surface = pygame.Surface((legend_rect.width, legend_rect.height), pygame.SRCALPHA)
            legend_surface.fill((40, 40, 40, 200))
            self.screen.blit(legend_surface, legend_rect)
            
            y_offset = 15
            if self.show_paths:
                path_text = self.ui.small_font.render("Blue: A* Chosen Path (V)", True, (0, 150, 255))
                self.screen.blit(path_text, (20, y_offset))
                y_offset += 20
            
            if self.show_all_paths:
                all_path_text = self.ui.small_font.render("Gray: A* Explored Paths (A)", True, (150, 150, 150))
                self.screen.blit(all_path_text, (20, y_offset))
                y_offset += 20
                
            if self.show_considered:
                path_text = self.ui.small_font.render("Purple: A* Considered Nodes (C)", True, (180, 20, 180))
                self.screen.blit(path_text, (20, y_offset))
                y_offset += 20
                
            if self.show_heatmap:
                heat_text = self.ui.small_font.render("Green-Red: Position Scores (H)", True, (255, 255, 0))
                self.screen.blit(heat_text, (20, y_offset))
    
    def _draw_path(self, path, color):
        """Draw a path with a given color"""
        if not path:
            return
            
        # Draw path cells
        for pos in path:
            # Skip positions with snakes for cleaner visualization
            if pos in self.snake1.body or pos in self.snake2.body:
                continue
                
            path_rect = pygame.Rect(
                pos[0] * CELL_SIZE,
                pos[1] * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            path_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            path_surface.fill(color)
            self.screen.blit(path_surface, path_rect)
        
        # Draw path direction arrows
        for i in range(len(path) - 1):
            current = path[i]
            next_pos = path[i + 1]
            direction = (next_pos[0] - current[0], next_pos[1] - current[1])
            self._draw_arrow(current, direction, color[:3])  # Use RGB part of color
            
    def _draw_arrow(self, pos, direction, color=(255, 255, 255)):
        """Draw an arrow showing path direction"""
        x, y = pos
        dx, dy = direction
        
        # Calculate arrow center coordinates
        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2
        
        # Calculate arrow points based on direction
        if dx == 1:  # Right
            points = [
                (center_x, center_y - 5),
                (center_x + 10, center_y),
                (center_x, center_y + 5)
            ]
        elif dx == -1:  # Left
            points = [
                (center_x, center_y - 5),
                (center_x - 10, center_y),
                (center_x, center_y + 5)
            ]
        elif dy == 1:  # Down
            points = [
                (center_x - 5, center_y),
                (center_x, center_y + 10),
                (center_x + 5, center_y)
            ]
        elif dy == -1:  # Up
            points = [
                (center_x - 5, center_y),
                (center_x, center_y - 10),
                (center_x + 5, center_y)
            ]
        else:
            return  # No valid direction
            
        # Draw the arrow
        pygame.draw.polygon(self.screen, color, points)
    
    def _draw_help(self):
        """Draw help overlay with keyboard controls"""
        # Create semi-transparent background
        help_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        help_surface.fill((0, 0, 0, 200))
        self.screen.blit(help_surface, (0, 0))
        
        # Create help content
        title = self.ui.title_font.render("Visualization Controls", True, (255, 255, 255))
        
        help_items = [
            ("V", "Toggle A* chosen path visualization"),
            ("A", "Toggle all explored A* paths"),
            ("H", "Toggle local search heatmap"),
            ("C", "Toggle A* considered nodes"),
            ("P", "Pause/unpause game"),
            ("F1", "Show/hide this help"),
            ("SPACE", "Restart game (when game over)")
        ]
        
        # Draw title
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Draw help items
        y_offset = 140
        for key, description in help_items:
            # Key box
            key_surface = self.ui.font.render(key, True, (255, 255, 255))
            key_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, y_offset, 50, 30)
            pygame.draw.rect(self.screen, (80, 80, 100), key_rect, 0, 5)
            self.screen.blit(key_surface, (key_rect.centerx - key_surface.get_width() // 2, 
                                          key_rect.centery - key_surface.get_height() // 2))
            
            # Description
            desc_surface = self.ui.font.render(description, True, (200, 200, 200))
            self.screen.blit(desc_surface, (SCREEN_WIDTH // 2 - 80, y_offset + 5))
            
            y_offset += 40
            
        # Close instruction
        close_text = self.ui.small_font.render("Press F1 to close this help", True, (180, 180, 255))
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(close_text, close_rect)
    
    def _draw_paused(self):
        """Draw paused indicator"""
        # Create semi-transparent overlay
        pause_surface = pygame.Surface((200, 60), pygame.SRCALPHA)
        pause_surface.fill((0, 0, 0, 150))
        
        # Position at bottom center
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
        self.screen.blit(pause_surface, pause_rect)
        
        # Draw text
        pause_text = self.ui.font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
        self.screen.blit(pause_text, text_rect)
        
        # Draw smaller instruction
        unpause_text = self.ui.small_font.render("Press P to unpause", True, (200, 200, 200))
        unpause_rect = unpause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        self.screen.blit(unpause_text, unpause_rect)