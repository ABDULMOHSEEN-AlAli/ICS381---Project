import random
import numpy as np
from collections import deque

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
        
        # Value settings for calculating position scores
        self.values = {
            'normal_food': 100,   # Normal food reward
            'super_food': 200,    # Super food reward
            'normal_move': 50,    # Normal move reward
            'trap': 15,           # Trap penalty
            'collision': 0        # Collision (worst case - avoid)
        }
        
        # Track previous positions to detect loops
        self.position_history = deque(maxlen=10)
        
        # Track successive moves without progress
        self.no_progress_count = 0
    
    def make_move(self):
        """Calculate the best move using local search and update the snake direction"""
        # Get current snake head position
        head_pos = self.snake.get_head_position()
        
        # Record current position for loop detection
        self.position_history.append(head_pos)
        
        # Get available directions
        available_directions = self.snake.get_available_dire(self.snake.direction)
        
        # If no available directions, just continue (shouldn't happen normally)
        if not available_directions:
            best_direction = self.snake.direction
            self.snake.update_move(best_direction)
        
        # Check for loops and increase exploration if needed
        exploration_factor = self.get_exploration_factor()
        
        # Evaluate each neighbor position
        direction_scores = []
        for direction in available_directions:
            next_pos = (head_pos[0] + direction[0], head_pos[1] + direction[1])
            
            # Skip invalid positions (collisions)
            if not self.is_valid_position(next_pos):
                continue
            
            # Calculate position score
            score = self.evaluate_position(next_pos, exploration_factor)
            direction_scores.append((direction, score))
        
        # If no valid moves, just continue (shouldn't happen normally)
        if not direction_scores:
            best_direction = self.snake.direction
            self.snake.update_move(best_direction)
        else:
            # Choose best direction based on score
            best_direction = max(direction_scores, key=lambda x: x[1])[0]
            
            # Check if we're making progress (getting closer to food or increasing score)
            if self.is_making_progress(head_pos, (head_pos[0] + best_direction[0], head_pos[1] + best_direction[1])):
                self.no_progress_count = 0
            else:
                self.no_progress_count += 1
            
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
    
    def evaluate_position(self, position, exploration_factor=0):
        """
        Evaluate a position based on multiple factors.
        Returns a score value - higher is better.
        """
        # Base score for valid moves
        score = self.values['normal_move']
        
        # Check for food
        score += self.food_score(position)
        
        # Check for traps
        score += self.trap_score(position)
        
        # Check for opponent proximity
        score += self.opponent_score(position)
        
        # Check proximity to walls
        score += self.wall_score(position)
        
        # Check for dead ends
        score += self.open_space_score(position)
        
        # Apply exploration factor to avoid loops
        if exploration_factor > 0:
            # Add randomness for exploration
            score += random.uniform(0, exploration_factor)
            
            # Penalize recently visited positions
            if position in self.position_history:
                score -= 50 * exploration_factor
        
        return score
    
    def food_score(self, position):
        """Calculate score based on food proximity and value"""
        score = 0
        
        # Bonus for being on food
        for food_pos, _ in self.food_manager.normal_food_items:
            if position == food_pos:
                return self.values['normal_food']
            
            # Smaller bonus for being near food
            dist = self.manhattan_distance(position, food_pos)
            if dist <= 5:
                score += self.values['normal_food'] * (6 - dist) / 10
        
        for food_pos, _ in self.food_manager.super_food_items:
            if position == food_pos:
                return self.values['super_food']
            
            # Smaller bonus for being near super food
            dist = self.manhattan_distance(position, food_pos)
            if dist <= 5:
                score += self.values['super_food'] * (6 - dist) / 10
        
        return score
    
    def trap_score(self, position):
        """Calculate score penalty for traps"""
        for trap_pos, _ in self.food_manager.spike_trap_items:
            if position == trap_pos:
                return -self.values['trap']
        
        return 0
    
    def opponent_score(self, position):
        """Calculate score penalty for being near opponent"""
        score = 0
        
        visible_segments = self.snake.radar(self.opponent)
        for segment in visible_segments:
            dist = self.manhattan_distance(position, segment)
            if dist <= 2:
                score -= (3 - dist) * 20
        
        return score
    
    def wall_score(self, position):
        """Calculate score penalty for being near walls"""
        score = 0
        
        # Penalty for being near walls
        x, y = position
        
        if x <= 1 or x >= self.grid.width - 2:
            score -= 10
        
        if y <= 1 or y >= self.grid.height - 2:
            score -= 10
        
        return score
    
    def open_space_score(self, position):
        """Calculate score based on available open space"""
        # Count available spaces in adjacent positions
        open_count = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            adj_pos = (position[0] + dx, position[1] + dy)
            if self.is_valid_position(adj_pos):
                open_count += 1
        
        # Bonus for positions with more open neighbors
        return open_count * 15
    
    def get_exploration_factor(self):
        """
        Determine how much exploration to do based on loop detection
        and lack of progress
        """
        # Check for position loops (visited same position multiple times)
        position_count = {}
        for pos in self.position_history:
            position_count[pos] = position_count.get(pos, 0) + 1
        
        # If any position appears multiple times, increase exploration
        max_visits = max(position_count.values()) if position_count else 0
        
        # Also factor in consecutive moves without progress
        exploration = max(max_visits - 1, self.no_progress_count / 3) 
        
        return min(exploration, 1.0)  # Cap at 1.0
    
    def is_making_progress(self, current_pos, next_pos):
        """
        Check if moving to next_pos is making progress
        (getting closer to food or score increase)
        """
        # Check if we'd be on food
        for food_pos, _ in self.food_manager.normal_food_items + self.food_manager.super_food_items:
            if next_pos == food_pos:
                return True
        
        # Find closest food from current and next positions
        closest_food = self.find_closest_food(current_pos)
        if closest_food:
            current_dist = self.manhattan_distance(current_pos, closest_food)
            next_dist = self.manhattan_distance(next_pos, closest_food)
            
            # We're making progress if we're getting closer to food
            if next_dist < current_dist:
                return True
        
        return False
    
    def find_closest_food(self, position):
        """Find the closest food item to the given position"""
        closest_food = None
        min_distance = float('inf')
        
        # Check all food items
        for food_pos, _ in self.food_manager.normal_food_items:
            dist = self.manhattan_distance(position, food_pos)
            if dist < min_distance:
                min_distance = dist
                closest_food = food_pos
        
        for food_pos, _ in self.food_manager.super_food_items:
            dist = self.manhattan_distance(position, food_pos)
            if dist < min_distance:
                min_distance = dist
                closest_food = food_pos
        
        return closest_food
    
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
