import pygame
from environment_constants import *
from random import randint
import random
import math
import time

class UI:
    def __init__(self, screen):
        self.screen = screen
        # Use pixelated fonts for authentic retro look
        pygame.font.init()
        try:
            # Try to load retro pixel fonts if available
            self.title_font = pygame.font.Font("Environment/fonts/retro_pixel.ttf", 32)
            self.font = pygame.font.Font("Environment/fonts/retro_pixel.ttf", 24)
            self.small_font = pygame.font.Font("Environment/fonts/retro_pixel.ttf", 20)
        except:
            # Fallback to system fonts with pixelated rendering
            self.title_font = pygame.font.SysFont('monospace', 32, bold=True)
            self.font = pygame.font.SysFont('monospace', 24, bold=True)
            self.small_font = pygame.font.SysFont('monospace', 20)
        
        # Classic arcade color palette
        self.neon_pink = (255, 20, 147)
        self.neon_blue = (0, 195, 255)
        self.neon_purple = (180, 0, 255)
        self.neon_green = (0, 255, 140)
        self.neon_yellow = (255, 240, 0)
        self.grid_colors = [(20, 10, 30), (25, 15, 35)]  # Dark grid colors
        
        # Create rounded rectangle surface for reuse
        self.rounded_rect_cache = {}
        
        # Time for animation effects
        self.time = 0
        self.real_start_time = time.time()
        
        # Load or create retro grid texture
        self.grid_texture = self.create_grid_texture()
        
        # CRT effect parameters
        self.crt_curve = 5  # CRT curvature strength
        self.noise_intensity = 0.03  # Static noise intensity
        
        # Create static noise once for reuse
        self.static_noise = self.generate_static_noise()
        
        # Create insert coin effect
        self.coin_flash_timer = 0
        self.high_score = 100  # Placeholder high score
        
        # Create arcade cabinet overlay
        self.cabinet_overlay = self.create_cabinet_overlay()
        
        # Create screen burn-in effect
        self.burn_in = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.burn_in.fill((20, 10, 30, 5))  # Slight purple tint
        
    def create_cabinet_overlay(self):
        """Create arcade cabinet overlay effect"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Dark corners to simulate arcade cabinet viewing angle
        corner_size = SCREEN_WIDTH // 3
        corner_alpha = 80
        
        # Top corners
        for x in range(corner_size):
            for y in range(corner_size):
                # Calculate distance from corner
                dist_tl = math.sqrt(x**2 + y**2) / corner_size
                dist_tr = math.sqrt((corner_size - x)**2 + y**2) / corner_size
                
                # Top-left corner
                if dist_tl < 1:
                    alpha = int(corner_alpha * (1 - dist_tl))
                    overlay.set_at((x, y), (0, 0, 0, alpha))
                
                # Top-right corner
                if dist_tr < 1:
                    alpha = int(corner_alpha * (1 - dist_tr))
                    overlay.set_at((SCREEN_WIDTH - x - 1, y), (0, 0, 0, alpha))
        
        # Bottom corners
        for x in range(corner_size):
            for y in range(corner_size):
                # Calculate distance from corner
                dist_bl = math.sqrt(x**2 + (corner_size - y)**2) / corner_size
                dist_br = math.sqrt((corner_size - x)**2 + (corner_size - y)**2) / corner_size
                
                # Bottom-left corner
                if dist_bl < 1:
                    alpha = int(corner_alpha * (1 - dist_bl))
                    overlay.set_at((x, SCREEN_HEIGHT - y - 1), (0, 0, 0, alpha))
                
                # Bottom-right corner
                if dist_br < 1:
                    alpha = int(corner_alpha * (1 - dist_br))
                    overlay.set_at((SCREEN_WIDTH - x - 1, SCREEN_HEIGHT - y - 1), (0, 0, 0, alpha))
                    
        # Add subtle radial gradient
        for x in range(SCREEN_WIDTH):
            for y in range(SCREEN_HEIGHT):
                # Distance from center (0 to 1)
                dx = (x - SCREEN_WIDTH/2) / (SCREEN_WIDTH/2)
                dy = (y - SCREEN_HEIGHT/2) / (SCREEN_HEIGHT/2)
                dist = min(1.0, math.sqrt(dx**2 + dy**2))
                
                # Stronger vignette toward edges
                if dist > 0.7:
                    alpha = int(60 * ((dist - 0.7) / 0.3))
                    current = overlay.get_at((x, y))
                    new_alpha = min(255, current[3] + alpha)
                    overlay.set_at((x, y), (current[0], current[1], current[2], new_alpha))
        
        return overlay
        
    def generate_static_noise(self):
        """Generate static noise texture for CRT effect"""
        noise_size = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)  # Smaller for optimization
        noise = pygame.Surface(noise_size, pygame.SRCALPHA)
        
        for x in range(noise_size[0]):
            for y in range(noise_size[1]):
                if random.random() < 0.5:
                    noise.set_at((x, y), (255, 255, 255, random.randint(0, 30)))
        
        return pygame.transform.scale(noise, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
    def create_grid_texture(self):
        """Create a retro grid texture for background"""
        texture_size = 512
        texture = pygame.Surface((texture_size, texture_size))
        texture.fill((20, 10, 30))  # Dark purple background
        
        # Draw horizontal grid lines
        for y in range(0, texture_size, 32):
            line_color = (60, 20, 120, 100)  # Neon purple, semi-transparent
            pygame.draw.line(texture, line_color, (0, y), (texture_size, y), 1)
        
        # Draw vertical grid lines
        for x in range(0, texture_size, 32):
            line_color = (60, 20, 120, 100)
            pygame.draw.line(texture, line_color, (x, 0), (x, texture_size), 1)
            
        # Add some "dirt/dust" pixels for authentic worn arcade look
        for _ in range(300):
            x = random.randint(0, texture_size-1)
            y = random.randint(0, texture_size-1)
            color = random.randint(30, 50)
            texture.set_at((x, y), (color, color, color))
        
        return texture

    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=(0, 0, 0), 
                          glow=False, glow_color=None, glow_size=5):
        """Draw a pixelated rounded rectangle with optional neon glow effect"""
        if radius < 1:
            pygame.draw.rect(surface, color, rect)
            if border:
                pygame.draw.rect(surface, border_color, rect, border)
            return
        
        # For retro pixelated look, use smaller radius
        radius = min(radius, 8)
        
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
            
            # Apply pixelation effect for retro look
            scaled_down = pygame.transform.scale(template, (rect.width // 4, rect.height // 4))
            pixelated = pygame.transform.scale(scaled_down, (rect.width, rect.height))
            
            self.rounded_rect_cache[cache_key] = pixelated.copy()
        
        # Create colored version using the cached template
        result = self.rounded_rect_cache[cache_key].copy()
        result.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        
        # Add neon glow effect
        if glow and glow_color:
            glow_surface = pygame.Surface((rect.width + glow_size*2, rect.height + glow_size*2), pygame.SRCALPHA)
            glow_rect = pygame.Rect(glow_size, glow_size, rect.width, rect.height)
            
            for i in range(glow_size, 0, -1):
                alpha = 150 * (1 - (i / glow_size))
                current_color = (*glow_color[:3], int(alpha))
                pygame.draw.rect(glow_surface, current_color, 
                               glow_rect.inflate(i*2, i*2), 0, radius + i//2)
                
            surface.blit(glow_surface, (rect.x - glow_size, rect.y - glow_size))
        
        # Draw to surface
        surface.blit(result, rect)
        
        # Draw border with pixelated effect
        if border > 0:
            border = max(2, border)  # Ensure visible border
            pygame.draw.rect(surface, border_color, rect, border, radius)

    def draw_scores(self, snake1_score, snake2_score, snake1_length=0, snake2_length=0):
        """Draw score display with retro arcade style"""
        # Background for score panel
        score_panel = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)
        
        # Create scanline effect
        for y in range(score_panel.y, score_panel.y + score_panel.height, 2):
            pygame.draw.line(self.screen, (10, 5, 15), 
                           (score_panel.x, y), 
                           (score_panel.x + score_panel.width, y), 1)
        
        # Draw background for score panel with CRT-like glow
        pygame.draw.rect(self.screen, (20, 5, 35), score_panel)
        
        # Draw snake 1 score box with neon effect
        snake1_box_width = 260
        snake1_box_height = 70
        snake1_box = pygame.Rect(10, SCREEN_HEIGHT - snake1_box_height - 5, snake1_box_width, snake1_box_height)
        
        # Pulsating glow effect based on time
        glow_intensity = 0.7 + 0.3 * math.sin(self.time / 10)
        glow_color = (int(self.neon_blue[0] * glow_intensity), 
                      int(self.neon_blue[1] * glow_intensity), 
                      int(self.neon_blue[2] * glow_intensity))
        
        self.draw_rounded_rect(self.screen, snake1_box, (40, 20, 80), 6, 2, self.neon_blue, 
                             glow=True, glow_color=glow_color, glow_size=4)
        
        # Add flickering effect to score boxes (occasional mild flicker)
        if random.random() < 0.02:  # 2% chance of flicker each frame
            flicker_intensity = random.uniform(0.8, 1.0)
            snake1_box_copy = self.screen.subsurface(snake1_box).copy()
            snake1_box_copy.set_alpha(int(255 * flicker_intensity))
            self.screen.blit(snake1_box_copy, snake1_box)
        
        # Draw snake 2 score box with neon effect
        snake2_box_width = 260
        snake2_box = pygame.Rect(SCREEN_WIDTH - snake2_box_width - 10, SCREEN_HEIGHT - snake1_box_height - 5,
                               snake2_box_width, snake1_box_height)
        
        glow_color = (int(self.neon_pink[0] * glow_intensity), 
                      int(self.neon_pink[1] * glow_intensity), 
                      int(self.neon_pink[2] * glow_intensity))
        
        self.draw_rounded_rect(self.screen, snake2_box, (80, 20, 40), 6, 2, self.neon_pink,
                             glow=True, glow_color=glow_color, glow_size=4)
        
        # Add occasional flicker to second box too
        if random.random() < 0.02:  # 2% chance of flicker
            flicker_intensity = random.uniform(0.8, 1.0)
            snake2_box_copy = self.screen.subsurface(snake2_box).copy()
            snake2_box_copy.set_alpha(int(255 * flicker_intensity))
            self.screen.blit(snake2_box_copy, snake2_box)
        
        # Draw retro-style labels with authentic 80s arcade font look
        snake1_label = self.font.render("P1", True, self.neon_blue)
        snake2_label = self.font.render("P2", True, self.neon_pink)
        
        # Draw text with CRT-like pixel effect
        self.screen.blit(snake1_label, (snake1_box.x + 20, snake1_box.y + 12))
        self.screen.blit(snake2_label, (snake2_box.x + 20, snake2_box.y + 12))
        
        # Draw pixel art divider with classic arcade feel
        for x in range(5):
            pygame.draw.rect(self.screen, self.neon_blue, 
                           (snake1_box.x + 60 + x*4, snake1_box.y + 18, 4, 4))
            pygame.draw.rect(self.screen, self.neon_pink, 
                           (snake2_box.x + 60 + x*4, snake2_box.y + 18, 4, 4))
        
        # Draw scores with authentic arcade styling - use zero-padding
        score1_text = self.font.render(f"{snake1_score:06d}", True, self.neon_yellow)
        score2_text = self.font.render(f"{snake2_score:06d}", True, self.neon_yellow)
        
        length1_text = self.small_font.render(f"LEN:{snake1_length:02d}", True, self.neon_green)
        length2_text = self.small_font.render(f"LEN:{snake2_length:02d}", True, self.neon_green)
        
        # Position scores with arcade-style spacing
        self.screen.blit(score1_text, (snake1_box.x + 100, snake1_box.y + 12))
        self.screen.blit(score2_text, (snake2_box.x + 100, snake2_box.y + 12))
        
        self.screen.blit(length1_text, (snake1_box.x + 20, snake1_box.y + 45))
        self.screen.blit(length2_text, (snake2_box.x + 20, snake2_box.y + 45))
        
        # Add arcade timer - show elapsed time
        elapsed_seconds = int(time.time() - self.real_start_time)
        mins = elapsed_seconds // 60
        secs = elapsed_seconds % 60
        time_text = self.font.render(f"TIME {mins:02d}:{secs:02d}", True, self.neon_green)
        
        # Draw time in the middle of score panel
        time_x = (SCREEN_WIDTH - time_text.get_width()) // 2
        self.screen.blit(time_text, (time_x, SCREEN_HEIGHT - 45))
        
        # Increment time for animation effects
        self.time += 0.5

    def draw_grid(self, grid_surface):
        """Draw the grid with synthwave sunset effect"""
        # Draw synthwave grid background
        grid_surface.fill((20, 10, 30))  # Dark purple background
        
        # Tile the grid texture for performance
        for x in range(0, GRID_WIDTH * CELL_SIZE, 512):
            for y in range(0, GRID_HEIGHT * CELL_SIZE, 512):
                grid_surface.blit(self.grid_texture, (x, y))
        
        # Add synthwave sun/horizon effect
        horizon_y = GRID_HEIGHT * CELL_SIZE * 0.7
        sun_radius = 100
        sun_center = (GRID_WIDTH * CELL_SIZE // 2, horizon_y)
        
        # Draw horizon line with gradient
        for y in range(int(horizon_y), GRID_HEIGHT * CELL_SIZE):
            alpha = 120 * (1 - (y - horizon_y) / (GRID_HEIGHT * CELL_SIZE - horizon_y))
            line_color = (230, 40, 100, int(alpha))  # Pink horizon
            pygame.draw.line(grid_surface, line_color, 
                           (0, y), (GRID_WIDTH * CELL_SIZE, y), 1)
        
        # Draw grid lines with retro effect
        for x in range(0, GRID_WIDTH * CELL_SIZE + 1, CELL_SIZE):
            # Perspective effect - lines converge to center
            start_x = x
            end_x = GRID_WIDTH * CELL_SIZE // 2 + (x - GRID_WIDTH * CELL_SIZE // 2) // 2
            pygame.draw.line(grid_surface, self.neon_purple, 
                           (start_x, 0), 
                           (end_x, horizon_y), 1)

        for y in range(0, GRID_HEIGHT * CELL_SIZE + 1, CELL_SIZE):
            pygame.draw.line(grid_surface, (60, 20, 80), 
                           (0, y), (GRID_WIDTH * CELL_SIZE, y), 1)
        
        # Add glowing grid border
        border_width = 4
        pygame.draw.rect(grid_surface, self.neon_purple, 
                       (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), border_width)
        
        # Add CRT scan lines effect
        for y in range(0, GRID_HEIGHT * CELL_SIZE, 4):
            pygame.draw.line(grid_surface, (0, 0, 0, 30), 
                           (0, y), (GRID_WIDTH * CELL_SIZE, y), 1)
        
        self.screen.blit(grid_surface, (0, 0))
        
        # Add random screen jitter (occasional)
        if random.random() < 0.01:  # 1% chance each frame
            jitter_x = random.randint(-2, 2)
            jitter_y = random.randint(-1, 1)
            self.screen.scroll(jitter_x, jitter_y)
        
        # Apply CRT "burn-in" effect - subtle persistent image
        self.screen.blit(self.burn_in, (0, 0))

    def draw_game_over(self, winner):
        """Draw game over message with authentic arcade aesthetic"""
        # Create CRT-like overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Darker overlay for contrast
        
        # Draw scan lines
        for y in range(0, SCREEN_HEIGHT, 2):
            pygame.draw.line(overlay, (0, 0, 0, 100), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Add vignette effect
        for radius in range(0, int(max(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.8), 4):
            alpha = int(180 * (radius / (max(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.8)))
            pygame.draw.circle(overlay, (0, 0, 0, alpha), 
                             (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 
                             max(SCREEN_WIDTH, SCREEN_HEIGHT) - radius, 1)
        
        self.screen.blit(overlay, (0, 0))
        
        # Create pixelated game over panel
        panel_width, panel_height = 500, 240  # Larger panel
        panel_rect = pygame.Rect((SCREEN_WIDTH - panel_width) // 2, 
                              (SCREEN_HEIGHT - panel_height) // 2,
                              panel_width, panel_height)
        
        # Dramatic glow effect based on winner
        if winner is None:
            glow_color = self.neon_purple
        elif winner.name == "Blue Snake":
            glow_color = self.neon_blue
        else:
            glow_color = self.neon_pink
            
        # Draw panel with glow effect
        self.draw_rounded_rect(self.screen, panel_rect, (40, 10, 60), 8, 3, glow_color,
                             glow=True, glow_color=glow_color, glow_size=10)
        
        # Game over title with authentic arcade font
        game_over_text = self.title_font.render("GAME  OVER", True, self.neon_yellow)
        
        # Classic arcade style - use double spaces between words
        
        # Draw pixelated text effect
        game_over_surface = pygame.Surface(game_over_text.get_size(), pygame.SRCALPHA)
        game_over_surface.blit(game_over_text, (0, 0))
        
        # Add glitch effect - occasionally displace pixels
        if random.random() < 0.2:  # 20% chance each frame
            x_offset = random.randint(-3, 3)
            glitch_rect = pygame.Rect(random.randint(0, game_over_text.get_width()-10), 
                                     0, 10, game_over_text.get_height())
            game_over_surface.blit(game_over_surface.subsurface(glitch_rect), 
                                 (glitch_rect.x + x_offset, glitch_rect.y))
        
        # Winner text
        if winner is None:
            winner_text = self.font.render("TIE  GAME!", True, self.neon_purple)
            color = self.neon_purple
        else:
            winner_color = self.neon_blue if winner.name == "Blue Snake" else self.neon_pink
            winner_text = self.font.render(f"PLAYER {1 if winner.name == 'Blue Snake' else 2}  WINS!", True, winner_color)
            color = winner_color
        
        # Score text with classic arcade styling
        if winner:
            score_text = self.font.render(f"SCORE  {winner.score:06d}", True, self.neon_green)
        else:
            score_text = self.font.render(f"NO  WINNER", True, self.neon_green)
        
        # Add arcade-style pixel particles
        if winner:
            for i in range(30):
                particle_size = random.randint(2, 6)
                x = random.randint(panel_rect.left + 20, panel_rect.right - 20)
                y = random.randint(panel_rect.top + 20, panel_rect.bottom - 20)
                # Pixelated square particles
                pygame.draw.rect(self.screen, color, (x, y, particle_size, particle_size))
        
        # Blinking "insert coin" text (classic arcade cabinet style)
        self.coin_flash_timer += 1
        if (self.coin_flash_timer // 15) % 2 == 0:  # Slower blinking
            coin_color = WHITE
        else:
            coin_color = self.neon_yellow
            
        restart_text = self.small_font.render("PRESS SPACE TO CONTINUE", True, coin_color)
        
        # Position and display text with authentic arcade spacing
        self.screen.blit(game_over_surface,
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                        panel_rect.top + 30))
        self.screen.blit(winner_text,
                       (SCREEN_WIDTH // 2 - winner_text.get_width() // 2,
                        panel_rect.top + 80))
        self.screen.blit(score_text,
                       (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                        panel_rect.top + 120))
        self.screen.blit(restart_text,
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                        panel_rect.top + 180))
        
        # Add high-score display (classic arcade staple)
        highscore_text = self.small_font.render(f"HI-SCORE  {self.high_score:06d}", True, self.neon_yellow)
        self.screen.blit(highscore_text,
                       (SCREEN_WIDTH // 2 - highscore_text.get_width() // 2,
                        panel_rect.bottom + 20))
        
        # Add copyright notice like old arcade games
        copyright_text = self.small_font.render("© 2025 ICS 381 CORP.", True, WHITE)
        self.screen.blit(copyright_text,
                       (SCREEN_WIDTH // 2 - copyright_text.get_width() // 2,
                        SCREEN_HEIGHT - 30))
            
        # Update the display to show the game over screen
        pygame.display.flip()
        
        # Wait specifically for space key to restart
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Allow quitting the game
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Only restart on space key
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:  # Allow exiting with ESC
                        pygame.quit()
                        exit()

    def draw_game_title(self):
        """Draw game title with authentic arcade cabinet style"""
        # Create title bar with scanlines
        title_bar = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(self.screen, (20, 5, 35), title_bar)
        
        # Add scanline effect
        for y in range(0, 60, 2):
            pygame.draw.line(self.screen, (10, 5, 20), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Title with color cycling effect - classic arcade attract mode
        cycle_speed = 0.05
        hue_shift = (math.sin(self.time * cycle_speed) + 1) / 2  # 0 to 1
        
        # Interpolate between neon colors
        r = int(self.neon_pink[0] * hue_shift + self.neon_blue[0] * (1 - hue_shift))
        g = int(self.neon_pink[1] * hue_shift + self.neon_blue[1] * (1 - hue_shift))
        b = int(self.neon_pink[2] * hue_shift + self.neon_blue[2] * (1 - hue_shift))
        title_color = (r, g, b)
        
        # Classic arcade titles used all caps and spaced letters
        title_text = self.title_font.render("S N A K E   A R C A D E", True, title_color)
        subtitle_text = self.small_font.render("ICS 381 © 2025", True, self.neon_green)
        
        # Pixelated title effect
        scaled_title = pygame.transform.scale(title_text, (title_text.get_width()//2, title_text.get_height()//2))
        pixelated_title = pygame.transform.scale(scaled_title, title_text.get_size())
        
        # Add typical arcade cabinet top border design
        for x in range(0, SCREEN_WIDTH, 16):
            if x % 32 == 0:
                color = self.neon_pink
            else:
                color = self.neon_blue
            pygame.draw.rect(self.screen, color, (x, 56, 8, 4))
        
        # Add random screen jitter/noise to title (occasional)
        if random.random() < 0.05:  # 5% chance each frame
            jitter_y = random.randint(-1, 1)
            title_pos_y = 10 + jitter_y
        else:
            title_pos_y = 10
        
        self.screen.blit(pixelated_title, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_pos_y))
        self.screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 40))
        
        # Apply CRT effects to entire screen
        self.apply_crt_effects()

    def apply_crt_effects(self):
        """Apply CRT monitor effects to the entire screen"""
        # Add subtle static noise (varies intensity based on time)
        noise_intensity = self.noise_intensity * (0.8 + 0.4 * math.sin(time.time() * 2))
        if noise_intensity > 0:
            # Generate new static each frame for authentic look
            static_noise = self.static_noise.copy()
            static_noise.set_alpha(int(255 * noise_intensity))
            self.screen.blit(static_noise, (0, 0), special_flags=pygame.BLEND_ADD)
        
        # Add occasional horizontal sync issues (line displacement)
        if random.random() < 0.005:  # 0.5% chance each frame
            line_y = random.randint(0, SCREEN_HEIGHT - 10)
            line_height = random.randint(2, 8)
            line_shift = random.randint(-10, 10)
            
            # Copy and shift a horizontal slice
            line_surf = self.screen.subsurface((0, line_y, SCREEN_WIDTH, line_height)).copy()
            self.screen.blit(line_surf, (line_shift, line_y))
        
        # Add the cabinet overlay for authentic arcade look
        self.screen.blit(self.cabinet_overlay, (0, 0))