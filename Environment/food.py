import pygame
import random
import os
from environment_constants import *


class FoodManager:
    def __init__(self, grid, snakes):
        self.grid = grid
        self.snakes = snakes # list of snakes
        # Store food with image references in table format
        self.normal_food_items = []
        self.super_food_items = []
        self.spike_trap_items = []

        # Load normal food images
        self.normal_food_images = self.load_images("Environment/images/Normal_Food")
        self.super_food_images = self.load_images("Environment/images/Super_Food")
        self.spike_trap_images = self.load_images("Environment/images/Traps")


        # Initialize food and Traps
        for _ in range(FOOD_AMOUNT):
            self.spawn_random_food()
        for _ in range(SPIKE_TRAPS_AMOUNT):
            self.spawn_spike_trap()


    def load_images(self, folder_path):
        """Loads all images from a given folder and scales them."""
        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".png"):
                img = pygame.image.load(os.path.join(folder_path, filename))
                img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
                images.append(img)
        return images

    def is_position_empty(self, position):
        """Check if a position is empty (no snakes, food, or Traps)"""
        # Check if position overlaps with any snake
        for snake in self.snakes:
            if position in snake.body:
                return False

        # Check if position overlaps with existing food or Traps
        for food_pos, _ in self.normal_food_items:
            if position == food_pos:
                return False

        for food_pos, _ in self.super_food_items:
            if position == food_pos:
                return False

        for trap_pos, _ in self.spike_trap_items:
            if position == trap_pos:
                return False

        return True

    def get_random_empty_position(self):
        """Get a random position that is not occupied by snakes or items"""
        position = None
        while position is None or not self.is_position_empty(position):
            x = random.randint(0, self.grid.width - 1)
            y = random.randint(0, self.grid.height - 1)
            position = (x, y)
        return position

    def spawn_normal_food(self):
        """Spawn normal food at a random location with a random image."""
        position = self.get_random_empty_position()
        image = random.choice(self.normal_food_images)
        self.normal_food_items.append((position, image))

    def spawn_super_food(self):
        """Spawn super food at a random location with a random image."""
        position = self.get_random_empty_position()
        image = random.choice(self.super_food_images)
        self.super_food_items.append((position, image))

    def spawn_spike_trap(self):
        """Spawn a spike trap at a random empty position"""
        position = self.get_random_empty_position()
        image = random.choice(self.spike_trap_images)
        self.spike_trap_items.append((position, image))

    def collect_item(self): # -> snake
        """Check if any snake has collected food or hit a trap"""
        for snake in self.snakes:
            head_pos = snake.get_head_position()

            # Check for normal food collection
            for i, (food_pos, _) in enumerate(self.normal_food_items[:]):
                if head_pos == food_pos:
                    self.normal_food_items.pop(i)
                    snake.grow(EXPANSION_RATE_NORMAL)
                    snake.score += 1
                    self.spawn_random_food()
                    break

            # Check for super food collection
            for i, (food_pos, _) in enumerate(self.super_food_items[:]):
                if head_pos == food_pos:
                    self.super_food_items.pop(i)
                    snake.grow(EXPANSION_RATE_SUPER)

                    # Random score between 1 and 3
                    score_increase = random.randint(1, 3)
                    snake.score += score_increase
                    self.spawn_random_food()
                    break

            # Check for spike trap collision
            for i, (trap_pos, _) in enumerate(self.spike_trap_items[:]):
                if head_pos == trap_pos:
                    self.spike_trap_items.pop(i)
                    isValid = snake.reduce_length()
                    snake.score = max(0, snake.score-1)
                    self.spawn_spike_trap()
                    if not isValid:
                        snake.score = -1
                    break

    def spawn_random_food(self):
        """Spawn either normal food or super food based on probability"""
        if random.random() < NORMAL_FOOD_PROB:
            self.spawn_normal_food()
        else:
            self.spawn_super_food()

    def draw(self, screen):
        """Draw all food items and Traps"""
        # Draw normal food
        for (x, y), image in self.normal_food_items:
            screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

        # Draw super food
        for (x, y), image in self.super_food_items:
            screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))

        # Draw spike Traps
        for (x, y), image in self.spike_trap_items:
            screen.blit(image, (x * CELL_SIZE, y * CELL_SIZE))