import pygame
from environment_constants import *


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.small_font = pygame.font.SysFont('arial', 20, bold=True)

    def draw_scores(self, snake1_score, snake2_score, snake1_length=0, snake2_length=0):
        """Draw score display at the bottom of the screen"""
        # Draw snake 1 score box (red)
        snake1_box_width = 260
        snake1_box_height = 80
        snake1_box = pygame.Rect(0, SCREEN_HEIGHT - snake1_box_height, snake1_box_width, snake1_box_height)
        pygame.draw.rect(self.screen, BLUE, snake1_box)
        pygame.draw.rect(self.screen, WHITE, snake1_box, 2)  # Add white border

        # Draw snake 2 score box (blue)
        snake2_box_width = 260
        snake2_box = pygame.Rect(SCREEN_WIDTH - snake2_box_width, SCREEN_HEIGHT - snake1_box_height,
                                 snake2_box_width, snake1_box_height)
        pygame.draw.rect(self.screen, ORANGE, snake2_box)
        pygame.draw.rect(self.screen, WHITE, snake2_box, 2)  # Add white border

        # Draw snake labels
        snake1_label = self.font.render("Snake 1", True, BLACK)
        snake2_label = self.font.render("Snake 2", True, WHITE)

        self.screen.blit(snake1_label, (snake1_box.centerx - snake1_label.get_width() // 2,
                                        snake1_box.y + 10))
        self.screen.blit(snake2_label, (snake2_box.centerx - snake2_label.get_width() // 2,
                                        snake2_box.y + 10))

        # Draw divider lines for score boxes
        pygame.draw.line(self.screen, WHITE, (snake1_box_width // 2, SCREEN_HEIGHT - snake1_box_height),
                         (snake1_box_width // 2, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE, (SCREEN_WIDTH - snake2_box_width // 2, SCREEN_HEIGHT - snake1_box_height),
                         (SCREEN_WIDTH - snake2_box_width // 2, SCREEN_HEIGHT), 2)

        # Draw scores and lengths
        score1_text = self.small_font.render(f"S: {snake1_score}", True, BLACK)
        length1_text = self.small_font.render(f"L: {snake1_length}", True, BLACK)
        score2_text = self.small_font.render(f"S: {snake2_score}", True, WHITE)
        length2_text = self.small_font.render(f"L: {snake2_length}", True, WHITE)

        # Position scores and lengths in their respective sections
        self.screen.blit(length1_text, (snake1_box_width // 4 - length1_text.get_width() // 2,
                                        SCREEN_HEIGHT - 40))
        self.screen.blit(score1_text, (snake1_box_width * 3 // 4 - score1_text.get_width() // 2,
                                       SCREEN_HEIGHT - 40))

        self.screen.blit(length2_text, (SCREEN_WIDTH - snake2_box_width * 3 // 4 - length2_text.get_width() // 2,
                                        SCREEN_HEIGHT - 40))
        self.screen.blit(score2_text, (SCREEN_WIDTH - snake2_box_width // 4 - score2_text.get_width() // 2,
                                       SCREEN_HEIGHT - 40))

    def draw_grid(self, grid_surface):
        """Draw the grid with border"""
        # Add border around the grid
        pygame.draw.rect(self.screen, WHITE,
                         (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)

        # Draw grid lines
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(grid_surface, WHITE, (x, 0), (x, GRID_HEIGHT * CELL_SIZE), 1)

        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(grid_surface, WHITE, (0, y), (GRID_WIDTH * CELL_SIZE, y), 1)

        self.screen.blit(grid_surface, (0, 0))

    def draw_game_over(self, winner):
        """Draw game over message with winner"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, WHITE)

        if winner is None:
            winner_text = self.font.render("It's a tie!", True, WHITE)
        else:
            winner_text = self.font.render(f"{winner.name} wins with {winner.score} points!", True, WHITE)

        restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)

        self.screen.blit(game_over_text,
                         (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                          SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(winner_text,
                         (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                          SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(restart_text,
                         (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                          SCREEN_HEIGHT // 2 + 20))