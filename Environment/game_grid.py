import pygame
from environment_constants import *


class Grid:
    def __init__(self):
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.cell_size = CELL_SIZE

    def is_valid_position(self, position):
        """Check if a position is within the grid boundaries"""
        x, y = position
        insideGrid = (x >= 0 and x < (self.width)) and (y >= 0 and y < (self.height))
        return insideGrid


    def draw(self, screen):
        """Draw the grid"""
        for x in range(self.width):
            for y in range(self.height):
                # Draw grid lines
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, GRID_COLOR, rect, 1)
