import pygame
from environment_constants import *
from random import randint
import random
import math

class UI:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init()
        # Use retro-style fonts
        self.title_font = pygame.font.Font(pygame.font.match_font('pressstart2p'), 32)
        self.font = pygame.font.Font(pygame.font.match_font('pressstart2p'), 16)
        self.small_font = pygame.font.Font(pygame.font.match_font('pressstart2p'), 12)
        
        # Retro color palette
        self.retro_colors = {
            'dark_blue': (20, 20, 60),
            'blue': (0, 0, 128),
            'orange': (128, 64, 0),
            'neon_green': (0, 255, 0),
            'neon_pink': (255, 20, 147),
            'neon_cyan': (0, 255, 255),
            'neon_yellow': (255, 255, 0)
        }
        
        # Load arcade cabinet overlay
        self.scan_line = self.create_scanline_overlay()
        self.timer = 0
        self.blink_state = False
        self.pixel_noise = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.update_pixel_noise()

    def create_scanline_overlay(self):
        """Create a scanline effect overlay"""
        scanline = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 3):
            pygame.draw.line(scanline, (0, 0, 0, 30), (0, y), (SCREEN_WIDTH, y))
        return scanline
    
    def update_pixel_noise(self):
        """Create CRT noise effect"""
        self.pixel_noise.fill((0, 0, 0))
        for _ in range(300):
            x = random.randint(0, SCREEN_WIDTH-1)
            y = random.randint(0, SCREEN_HEIGHT-1)
            brightness = random.randint(0, 50)
            pygame.draw.rect(self.pixel_noise, (brightness, brightness, brightness), (x, y, 2, 2))

    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=(0, 0, 0)):
        """Draw a rounded rectangle with optional border"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        if border > 0:
            pygame.draw.rect(surface, border_color, rect, width=border, border_radius=radius)

    def draw_retro_emboss(self, surface, rect, color, radius=10):
        """Draw a retro-style embossed rectangle"""
        # Main rect
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
        # Dark edge (bottom-right)
        dark_edge = pygame.Rect(rect.left+3, rect.top+3, rect.width-3, rect.height-3)
        pygame.draw.rect(surface, (color[0]//2, color[1]//2, color[2]//2), dark_edge, 
                         width=3, border_radius=radius-1)
        
        # Light edge (top-left)
        light_color = (min(color[0]+50, 255), min(color[1]+50, 255), min(color[2]+50, 255))
        pygame.draw.line(surface, light_color, (rect.left+2, rect.bottom-radius), 
                        (rect.left+2, rect.top+radius), 3)
        pygame.draw.line(surface, light_color, (rect.left+radius, rect.top+2), 
                        (rect.right-radius, rect.top+2), 3)

    def draw_scores(self, snake1_score, snake2_score, snake1_length=0, snake2_length=0):
        """Draw score display at the bottom of the screen with retro visuals"""
        # Retro-style score panel with grid pattern
        score_panel = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        pygame.draw.rect(self.screen, self.retro_colors['dark_blue'], score_panel)
        
        # Draw grid lines on score panel
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.screen, (40, 40, 80), (x, SCREEN_HEIGHT - 80), (x, SCREEN_HEIGHT), 1)
        for y in range(SCREEN_HEIGHT - 80, SCREEN_HEIGHT, 10):
            pygame.draw.line(self.screen, (40, 40, 80), (0, y), (SCREEN_WIDTH, y), 1)

        # Snake 1 score box
        snake1_box = pygame.Rect(10, SCREEN_HEIGHT - 75, 260, 70)
        self.draw_retro_emboss(self.screen, snake1_box, self.retro_colors['blue'], 8)

        # Snake 2 score box
        snake2_box = pygame.Rect(SCREEN_WIDTH - 270, SCREEN_HEIGHT - 75, 260, 70)
        self.draw_retro_emboss(self.screen, snake2_box, self.retro_colors['orange'], 8)

        # Snake labels with neon glow effect
        snake1_label = self.font.render("BLUE SNAKE", True, self.retro_colors['neon_cyan'])
        snake2_label = self.font.render("ORANGE SNAKE", True, self.retro_colors['neon_yellow'])
        
        # Draw glow effect
        glow_surface = pygame.Surface((snake1_label.get_width()+10, snake1_label.get_height()+10), pygame.SRCALPHA)
        glow_surface.fill((0,0,0,0))
        for i in range(5, 0, -1):
            alpha = 50 - i*10
            pygame.draw.rect(glow_surface, (0, 255, 255, alpha), 
                            (5-i, 5-i, snake1_label.get_width()+i*2, snake1_label.get_height()+i*2))
        
        self.screen.blit(glow_surface, (snake1_box.x + 5, snake1_box.y + 5))
        self.screen.blit(snake1_label, (snake1_box.x + 10, snake1_box.y + 10))
        self.screen.blit(snake2_label, (snake2_box.x + 10, snake2_box.y + 10))

        # Scores and lengths with arcade-style display
        score1_text = self.small_font.render(f"SCORE: {snake1_score}", True, (255, 255, 255))
        length1_text = self.small_font.render(f"LENGTH: {snake1_length}", True, (255, 255, 255))
        score2_text = self.small_font.render(f"SCORE: {snake2_score}", True, (255, 255, 255))
        length2_text = self.small_font.render(f"LENGTH: {snake2_length}", True, (255, 255, 255))

        self.screen.blit(score1_text, (snake1_box.x + 10, snake1_box.y + 40))
        self.screen.blit(length1_text, (snake1_box.x + 140, snake1_box.y + 40))
        self.screen.blit(score2_text, (snake2_box.x + 10, snake2_box.y + 40))
        self.screen.blit(length2_text, (snake2_box.x + 140, snake2_box.y + 40))

    def draw_grid(self, grid_surface):
        """Draw the grid with enhanced retro visuals"""
        # Draw classic grid pattern
        for y in range(0, GRID_HEIGHT):
            for x in range(0, GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = (30, 30, 50) if (x + y) % 2 == 0 else (20, 20, 40)
                pygame.draw.rect(grid_surface, color, rect)
                # Add subtle grid lines
                pygame.draw.line(grid_surface, (40, 40, 60), 
                                (x * CELL_SIZE, y * CELL_SIZE), 
                                (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE), 1)
                pygame.draw.line(grid_surface, (40, 40, 60), 
                                (x * CELL_SIZE, y * CELL_SIZE), 
                                (x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE), 1)

        # Add neon glowing border with pulsating effect
        pulse = (math.sin(self.timer / 15) + 1) * 50 + 150  # Value between 150-250
        border_color = (pulse, pulse, 255)
        pygame.draw.rect(grid_surface, border_color, 
                        (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 3)
        
        # Add inner border
        pygame.draw.rect(grid_surface, (50, 50, 100), 
                        (3, 3, GRID_WIDTH * CELL_SIZE - 6, GRID_HEIGHT * CELL_SIZE - 6), 1)
                        
        self.screen.blit(grid_surface, (0, 0))

    def draw_game_over(self, winner):
        """Draw game over message with enhanced retro visuals"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Game over panel with arcade cabinet style
        panel_width, panel_height = 450, 200
        panel_rect = pygame.Rect((SCREEN_WIDTH - panel_width) // 2, 
                                (SCREEN_HEIGHT - panel_height) // 2,
                                panel_width, panel_height)
        self.draw_retro_emboss(self.screen, panel_rect, (0, 0, 80), 10)
        
        # Add decorative corners
        corner_size = 15
        for corner in [
            (panel_rect.left + 5, panel_rect.top + 5),
            (panel_rect.right - corner_size - 5, panel_rect.top + 5),
            (panel_rect.left + 5, panel_rect.bottom - corner_size - 5),
            (panel_rect.right - corner_size - 5, panel_rect.bottom - corner_size - 5)
        ]:
            pygame.draw.rect(self.screen, self.retro_colors['neon_pink'], 
                            (corner[0], corner[1], corner_size, corner_size))

        # Game over text with blinking effect
        game_over_text = self.title_font.render("GAME OVER", True, 
                                              (255, 0, 0) if self.blink_state else (180, 0, 0))
        text_shadow = self.title_font.render("GAME OVER", True, (100, 0, 0))
        
        # Draw text shadow
        self.screen.blit(text_shadow, 
                        (SCREEN_WIDTH // 2 - text_shadow.get_width() // 2 + 3, 
                         panel_rect.y + 23))
        # Draw main text
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         panel_rect.y + 20))

        # Winner text with arcade style
        if winner is None:
            winner_text = self.font.render("IT'S A TIE!", True, self.retro_colors['neon_yellow'])
        else:
            winner_color = self.retro_colors['neon_cyan'] if winner.name == "Blue Snake" else self.retro_colors['neon_yellow']
            winner_text = self.font.render(f"{winner.name.upper()} WINS!", True, winner_color)
        
        self.screen.blit(winner_text, 
                        (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, 
                         panel_rect.y + 80))

        # High score style display
        score_text = self.small_font.render("FINAL SCORES", True, (255, 255, 255))
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                         panel_rect.y + 110))

        # Restart instruction with blinking effect
        if self.blink_state:
            restart_text = self.small_font.render("PRESS SPACE TO RESTART", True, self.retro_colors['neon_green'])
            self.screen.blit(restart_text, 
                            (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                            panel_rect.y + 155))

    def draw_game_title(self):
        """Draw game title at the top of the screen with enhanced retro visuals"""
        # Draw arcade-style title banner
        banner_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(self.screen, (0, 0, 40), banner_rect)
        
        # Draw decorative patterns
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(self.screen, (30, 30, 60), (x, 0, 20, 5))
            pygame.draw.rect(self.screen, (30, 30, 60), (x+20, 65, 20, 5))
            
        # Create title with neon glow effect
        title_text = self.title_font.render("SNAKE AI COMPETITION", True, self.retro_colors['neon_green'])
        subtitle_text = self.small_font.render("RETRO ARCADE EDITION", True, self.retro_colors['neon_pink'])
        
        # Add glow effect to title
        glow_size = int(math.sin(self.timer / 10) * 3) + 5  # Pulsating glow
        glow_surface = pygame.Surface((title_text.get_width() + glow_size*2, 
                                      title_text.get_height() + glow_size*2), pygame.SRCALPHA)
        for i in range(glow_size, 0, -1):
            alpha = 10 + (glow_size - i) * 5
            color = self.retro_colors['neon_green'] + (alpha,)
            pygame.draw.rect(glow_surface, color, 
                           (glow_size-i, glow_size-i, 
                            title_text.get_width()+i*2, title_text.get_height()+i*2),
                           border_radius=5)

        # Blit glow and text
        self.screen.blit(glow_surface, 
                        (SCREEN_WIDTH // 2 - (title_text.get_width() + glow_size*2) // 2, 
                         5 - glow_size))
        self.screen.blit(title_text, 
                        (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
        self.screen.blit(subtitle_text, 
                        (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 45))

    def apply_retro_effects(self):
        """Apply advanced retro CRT and arcade cabinet effects"""
        # Update timer and effects
        self.timer += 1
        if self.timer % 30 == 0:
            self.blink_state = not self.blink_state
        
        if self.timer % 4 == 0:
            self.update_pixel_noise()
        
        # RGB color shift effect (subtle chromatic aberration)
        rgb_shift = abs(int(math.sin(self.timer * 0.01) * 2))
        if rgb_shift > 0:
            red_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            blue_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            red_surface.blit(self.screen, (-rgb_shift, 0))
            blue_surface.blit(self.screen, (rgb_shift, 0))
            
            self.screen.blit(red_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.screen.blit(blue_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Apply scan lines with varying intensity
        scan_alpha = int(115 + 15 * math.sin(self.timer * 0.1))
        self.scan_line.set_alpha(scan_alpha)
        self.screen.blit(self.scan_line, (0, 0))
        
        # Apply subtle noise with variable intensity
        noise_alpha = 30 + int(10 * math.sin(self.timer * 0.2))
        self.pixel_noise.set_alpha(noise_alpha)
        self.screen.blit(self.pixel_noise, (0, 0), special_flags=pygame.BLEND_ADD)
        
        # Random screen jitter effect (very subtle)
        if random.random() < 0.005:
            jitter_amount = random.randint(1, 3)
            jitter_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            jitter_surface.blit(self.screen, (0, 0))
            self.screen.blit(jitter_surface, (0, -jitter_amount))
        
        # CRT vignette effect (darker rounded corners)
        vignette = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        max_dist = math.sqrt((SCREEN_WIDTH // 2)**2 + (SCREEN_HEIGHT // 2)**2)
        
        for x in range(0, SCREEN_WIDTH, 2):
            for y in range(0, SCREEN_HEIGHT, 2):
                distance = math.sqrt((x - center[0])**2 + (y - center[1])**2)
                alpha = int(min(255, (distance / max_dist) * 320))
                pygame.draw.rect(vignette, (0, 0, 0, alpha), (x, y, 2, 2))
        
        # Apply pulsating brightness to vignette
        pulse = 0.7 + 0.1 * math.sin(self.timer * 0.05)
        vignette.set_alpha(int(180 * pulse))
        self.screen.blit(vignette, (0, 0), special_flags=pygame.BLEND_MULTIPLY)
        
        # Occasional screen flicker effect
        if random.random() < 0.002:
            flicker = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flicker.fill((20, 20, 20))
            self.screen.blit(flicker, (0, 0), special_flags=pygame.BLEND_ADD)

    def update(self):
        """Update UI animations and effects"""
        self.apply_retro_effects()
