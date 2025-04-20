import pygame
from environment_constants import *
from random import randint
import random

class UI:
    def __init__(self, screen):
        self.screen = screen
        # Use better fonts with more variety
        pygame.font.init()
        self.title_font = pygame.font.SysFont('monospace', 32, bold=True)
        self.font = pygame.font.SysFont('monospace', 24, bold=True)
        self.small_font = pygame.font.SysFont('monospace', 20)
        
        # Create rounded rectangle surface for reuse
        self.rounded_rect_cache = {}

    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=(0, 0, 0)):
        """Draw a rounded rectangle with optional border"""
        if radius < 1:
            pygame.draw.rect(surface, color, rect)
            if border:
                pygame.draw.rect(surface, border_color, rect, border)
            return
        
        # Cache key based on dimensions and radius
        cache_key = (rect.width, rect.height, radius)
        
        if cache_key not in self.rounded_rect_cache:
            # Create a new surface for this size with transparent background
            corner = pygame.Surface((radius, radius), pygame.SRCALPHA)
            pygame.draw.circle(corner, (255, 255, 255), (radius, radius), radius)
            corner_bl = pygame.transform.flip(corner, False, True)
            corner_tr = pygame.transform.flip(corner, True, False)
            corner_br = pygame.transform.flip(corner, True, True)
            
            # Create template surface
            template = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            template.fill((0, 0, 0, 0))
            
            # Add corners to template
            template.blit(corner, (0, 0))
            template.blit(corner_tr, (rect.width - radius, 0))
            template.blit(corner_bl, (0, rect.height - radius))
            template.blit(corner_br, (rect.width - radius, rect.height - radius))
            
            # Fill rest of template
            pygame.draw.rect(template, (255, 255, 255), (radius, 0, rect.width - radius * 2, rect.height))
            pygame.draw.rect(template, (255, 255, 255), (0, radius, rect.width, rect.height - radius * 2))
            
            self.rounded_rect_cache[cache_key] = template.copy()
        
        # Create colored version using the cached template
        result = self.rounded_rect_cache[cache_key].copy()
        result.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        
        # Draw to surface
        surface.blit(result, rect)
        
        # Draw border if needed
        if border > 0:
            # Create a slightly larger rect for the border
            border_rect = rect.inflate(border, border)
            border_surface = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
            
            # Draw outer and inner rounded rects for border effect
            inner_rect = pygame.Rect(border, border, rect.width, rect.height)
            self.draw_rounded_rect(border_surface, pygame.Rect(0, 0, border_rect.width, border_rect.height), border_color, radius + border)
            self.draw_rounded_rect(border_surface, inner_rect, (0, 0, 0, 0), radius)
            
            surface.blit(border_surface, rect.move(-border // 2, -border // 2))

    def draw_scores(self, snake1_score, snake2_score, snake1_length=0, snake2_length=0):
        """Draw score display at the bottom of the screen with enhanced visuals"""
        # Background for score panel
        score_panel = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, (40, 40, 40), score_panel)
        
        # Draw snake 1 score box with enhanced design
        snake1_box_width = 260
        snake1_box_height = 70
        snake1_box = pygame.Rect(10, SCREEN_HEIGHT - snake1_box_height - 5, snake1_box_width, snake1_box_height)
        self.draw_rounded_rect(self.screen, snake1_box, BLUE, 15, 2, (20, 60, 120))
        
        # Draw snake 2 score box with enhanced design
        snake2_box_width = 260
        snake2_box = pygame.Rect(SCREEN_WIDTH - snake2_box_width - 10, SCREEN_HEIGHT - snake1_box_height - 5,
                                 snake2_box_width, snake1_box_height)
        self.draw_rounded_rect(self.screen, snake2_box, ORANGE, 15, 2, (120, 60, 20))
        
        # Draw snake labels with shadow effect
        snake1_label = self.font.render("Blue Snake", True, WHITE)
        snake2_label = self.font.render("Orange Snake", True, WHITE)
        
        # Add subtle shadows
        shadow_offset = 2
        snake1_shadow = self.font.render("Blue Snake", True, (20, 60, 120))
        snake2_shadow = self.font.render("Orange Snake", True, (120, 60, 20))
        
        self.screen.blit(snake1_shadow, (snake1_box.centerx - snake1_label.get_width() // 2 + shadow_offset,
                                      snake1_box.y + 12 + shadow_offset))
        self.screen.blit(snake1_label, (snake1_box.centerx - snake1_label.get_width() // 2,
                                      snake1_box.y + 12))
        
        self.screen.blit(snake2_shadow, (snake2_box.centerx - snake2_label.get_width() // 2 + shadow_offset,
                                      snake2_box.y + 12 + shadow_offset))
        self.screen.blit(snake2_label, (snake2_box.centerx - snake2_label.get_width() // 2,
                                      snake2_box.y + 12))
        
        # Draw divider lines with glow effect
        pygame.draw.line(self.screen, (150, 150, 255), (snake1_box.centerx, snake1_box.y + 10),
                         (snake1_box.centerx, snake1_box.y + snake1_box_height - 10), 3)
        pygame.draw.line(self.screen, (255, 150, 100), (snake2_box.centerx, snake2_box.y + 10),
                         (snake2_box.centerx, snake2_box.y + snake1_box_height - 10), 3)
        
        # Draw scores and lengths with icons
        score1_text = self.small_font.render(f"SCORE: {snake1_score}", True, WHITE)
        length1_text = self.small_font.render(f"LENGTH: {snake1_length}", True, WHITE)
        score2_text = self.small_font.render(f"SCORE: {snake2_score}", True, WHITE)
        length2_text = self.small_font.render(f"LENGTH: {snake2_length}", True, WHITE)
        
        # Position scores and lengths with better spacing
        self.screen.blit(length1_text, (snake1_box.x + 20, snake1_box.y + 45))
        self.screen.blit(score1_text, (snake1_box.centerx + 20, snake1_box.y + 45))
        self.screen.blit(length2_text, (snake2_box.x + 20, snake2_box.y + 45))
        self.screen.blit(score2_text, (snake2_box.centerx + 20, snake2_box.y + 45))

    def draw_grid(self, grid_surface):
        """Draw the grid with enhanced visuals"""
        # Add gradient background for the grid
        for y in range(0, GRID_HEIGHT):
            intensity = 20 + int((y / GRID_HEIGHT) * 30)
            color = (intensity, intensity, intensity + 10)
            pygame.draw.rect(grid_surface, color, 
                            (0, y * CELL_SIZE, GRID_WIDTH * CELL_SIZE, CELL_SIZE))
        
        # Add subtle grid pattern
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(grid_surface, (60, 60, 70), (x, 0), (x, GRID_HEIGHT * CELL_SIZE), 1)

        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(grid_surface, (60, 60, 70), (0, y), (GRID_WIDTH * CELL_SIZE, y), 1)
        
        # Add glowing border around the grid
        border_width = 3
        pygame.draw.rect(grid_surface, (80, 80, 100), 
                       (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), border_width)
        
        self.screen.blit(grid_surface, (0, 0))

    def draw_game_over(self, winner):
        """Draw game over message with enhanced visuals"""
        # Create gradient overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(SCREEN_HEIGHT):
            alpha = int(180 * (1 - abs((y - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT // 2))))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (SCREEN_WIDTH, y))
        self.screen.blit(overlay, (0, 0))
        
        # Create game over panel
        panel_width, panel_height = 500, 200
        panel_rect = pygame.Rect((SCREEN_WIDTH - panel_width) // 2, 
                                (SCREEN_HEIGHT - panel_height) // 2,
                                panel_width, panel_height)
        self.draw_rounded_rect(self.screen, panel_rect, (40, 40, 60), 20, 3, (100, 100, 140))
        
        # Game over title with glow effect
        game_over_text = self.title_font.render("GAME OVER", True, (255, 220, 100))
        
        # Winner text
        if winner is None:
            winner_text = self.font.render("It's a tie!", True, WHITE)
            color = (200, 200, 200)
        else:
            winner_color = BLUE if winner.name == "Blue Snake" else ORANGE
            winner_text = self.font.render(f"{winner.name} wins with {winner.score} points!", True, winner_color)
            color = winner_color
        
        # Add particle effect for winner
        if winner:
            for i in range(20):
                particle_size = random.randint(3, 8)
                x = random.randint(panel_rect.left + 20, panel_rect.right - 20)
                y = random.randint(panel_rect.top + 20, panel_rect.bottom - 20)
                pygame.draw.circle(self.screen, color, (x, y), particle_size)
        
        restart_text = self.small_font.render("Press SPACE to restart", True, (180, 180, 255))
        
        self.screen.blit(game_over_text,
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                        panel_rect.top + 40))
        self.screen.blit(winner_text,
                       (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                        panel_rect.top + 90))
        self.screen.blit(restart_text,
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                        panel_rect.top + 140))

    def draw_game_title(self):
        """Draw game title at the top of the screen"""
        title_text = self.title_font.render("SNAKE AI COMPETITION", True, (255, 255, 255))
        subtitle_text = self.small_font.render("ICS 381 Project", True, (200, 200, 200))
        
        # Draw with shadow effect
        shadow_offset = 2
        title_shadow = self.title_font.render("SNAKE AI COMPETITION", True, (50, 50, 70))
        subtitle_shadow = self.small_font.render("ICS 381 Project", True, (50, 50, 70))
        
        # Add to top of grid
        overlay_height = 40
        pygame.draw.rect(self.screen, (30, 30, 45), (0, -5, SCREEN_WIDTH, overlay_height))
        
        self.screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + shadow_offset, 
                                     10 + shadow_offset))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
        
        self.screen.blit(subtitle_shadow, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2 + shadow_offset, 
                                       40 + shadow_offset))
        self.screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 40))