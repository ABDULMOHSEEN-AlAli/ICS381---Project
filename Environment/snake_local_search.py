import random
import numpy as np
from environment_constants import *

class SnakeLocalSearch:
    """
    Snake AI using a local search algorithm that evaluates nearby positions
    and selects the best one based on various factors.
    """
    
    def __init__(self, snake, opponent, grid, food_manager):
        self.snake = snake
        self.opponent = opponent
        self.grid = grid
        self.food_manager = food_manager
        
        # Value settings for calculating costs/rewards
        self.values = {
            'normal_food_reward': NORMAL_FOOD_REWARD,   # Normal food reward
            'super_food_reward': SUPER_FOOD_REWARD,    # Super food reward

            'normal_food_cost': NORMAL_FOOD_COST,  # Cost of normal food
            'super_food_cost': SUPER_FOOD_COST,    # Cost of super food
            'normal_move_cost': SAVE_MOVE_COST,    # Normal move cost
            'trap_cost': SPIKE_TRAP_COST,           # Trap cost
        }
    
    def make_move(self):
        """Calculate the best move using local search and update the snake direction"""
        # Get current snake head position
        head_pos = self.snake.get_head_position()
        
        # Get available directions
        available_directions = self.snake.get_available_dire(self.snake.direction)
        
        # If no available directions, just continue 
        if not available_directions:
            best_direction = self.snake.direction
            self.snake.update_move(best_direction)
        
        # Evaluate each neighbor position
        direction_scores = []
        for direction in available_directions:
            next_pos = (head_pos[0] + direction[0], head_pos[1] + direction[1])
            
            # Skip invalid positions (collisions)
            if not self.is_valid_position(next_pos):
                continue
            
            # Calculate position score
            score = self.evaluate_position(next_pos)
            direction_scores.append((direction, score))
        direction_names = {(0, -1): "UP", (0, 1): "DOWN", (-1, 0): "LEFT", (1, 0): "RIGHT"}
        readable_scores = [(direction_names.get(direction, direction), score) for direction, score in direction_scores]
        # print("Direction scores:", readable_scores)
        if not direction_scores:
            best_direction = self.snake.direction
            self.snake.update_move(best_direction)
        else:
            # Choose best direction based on score

            min_score = min(direction_scores, key=lambda x: x[1])[1]
            best_directions = [direction for direction, score in direction_scores if score == min_score]
            # print("Best directions:", best_directions)
            best_direction = random.choice(best_directions)

            
            # Update snake direction
            self.snake.update_move(best_direction)
    
    def is_valid_position(self, position):
        """Check if a position is valid (not a collision)"""
        # Check grid boundaries
        if not self.grid.is_valid_position(position):
            return False
        
        # Check collision with own body (except tail which will move)
        if position in self.snake.body[:-1]:
            return False
        
        # Check collision with opponent
        if position in self.opponent.body:
            return False
        
        return True
    
    def evaluate_position(self, position):
        """
        Evaluate a position based on multiple factors.
        Returns a score value - higher is better.
        """

        normal_food_items = [item[0] for item in self.food_manager.normal_food_items]
        super_food_items = [item[0] for item in self.food_manager.super_food_items]
        spike_trap_items = [item[0] for item in self.food_manager.spike_trap_items]

        if position in spike_trap_items:
            return self.values['trap_cost']
        
        elif position in super_food_items or position in normal_food_items:
            return self.values['normal_food_cost']
        
        else:
            return self.food_score(position)

    
    
    def food_score(self, position):
        """Calculate score based on food proximity and value"""
        best_dist = float('inf')

        for food_pos, _ in self.food_manager.normal_food_items:      
            dist = self.manhattan_distance(position, food_pos)
            if dist < best_dist:
                best_dist = dist
        for food_pos, _ in self.food_manager.super_food_items:
            dist = self.manhattan_distance(position, food_pos)
            if dist < best_dist:
                best_dist = dist
        
        return (best_dist * 5) + self.values["normal_food_cost"] # based on 300/28.5 = 10.5263
    
    
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class LocalSearchAI:
    """
    Interface class for the Snake Local Search Algorithm.
    Use this class in your game_logic.py.
    """
    def __init__(self, snake, opponent, grid, food_manager):
        self.ai = SnakeLocalSearch(snake, opponent, grid, food_manager)
    
    def make_move(self):
        """Calculate and execute the next move"""
        self.ai.make_move()