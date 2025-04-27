import heapq
from collections import defaultdict
from environment_constants import *

class SnakeAI:
    """
    Simple A* Algorithm implementation for the Snake game based on ICS381 course concepts.
    This agent uses A* search to find optimal paths to food while avoiding obstacles.
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
        
        # Available directions
        self.directions = {
            'UP':   UP,
            'DOWN': DOWN,
            'LEFT': LEFT,
            'RIGHT': RIGHT
        }
    
    def make_move(self):
        """Calculate the best move using A* and update the snake's direction"""
        # Get current snake head position
        head_pos = self.snake.get_head_position()
        
        # Find best target (food item)
        target = self.find_best_target()
        

        # Find path to target using A*
        path = self.a_star_search(head_pos, target)
        
        if path and len(path) > 1:
            # Get the first move in the path
            next_pos = path[1]  # Skip current position
            
            # Convert to direction vector
            dx = next_pos[0] - head_pos[0]
            dy = next_pos[1] - head_pos[1]
            direction = (dx, dy)
            
            # Update snake direction
            self.snake.update_move(direction)
        else:
            # No valid path found, keep current direction
            self.snake.update_move(self.snake.direction)

    
    def find_best_target(self):
        """Find the best food target based on value and distance"""
        head_pos = self.snake.get_head_position()
        best_target = None
        best_value = float('-inf')
        
        # Check normal food items
        for food_pos, _ in self.food_manager.normal_food_items:
            distance = self.manhattan_distance(head_pos, food_pos)
            value = self.values['normal_food_reward'] - (distance * 5)  # Value decreases with distance
            
            if value > best_value:
                best_value = value
                best_target = food_pos
        
        # Check super food items (higher value)
        for food_pos, _ in self.food_manager.super_food_items:
            distance = self.manhattan_distance(head_pos, food_pos)
            value = self.values['super_food_reward'] - (distance * 5)
            
            if value > best_value:
                best_value = value
                best_target = food_pos
        
        return best_target
    
    def a_star_search(self, head_pos, goal):
        """A* search algorithm to find path from start to goal"""
        # Priority queue for open set, format: (f_score, position)
        open_set = []
        heapq.heappush(open_set, (0, head_pos)) # It is an efficient priority queue implementation
        
        # For path reconstruction
        came_from = {}
        
        # actual_score[position] = cost from start to position
        actual_score = defaultdict(lambda: float('inf'))
        actual_score[head_pos] = 0
        
        f_score = defaultdict(lambda: float('inf'))
        f_score[head_pos] = self.heuristic(head_pos, goal)
        
        # To prevent infinite loops
        closed_set = set()
        
        while open_set:
            # Get position with lowest f_score
            _, current = heapq.heappop(open_set)
            
            # If we reached the goal
            if current == goal:
                # Reconstruct and return the path
                return self.reconstruct_path(came_from, current)
            
            # Add to closed set to avoid revisiting
            closed_set.add(current)
            
            # Get available moves from current position
            available_dirs = self.get_available_directions(current)
            
            for direction in available_dirs:
                # Calculate neighbor position
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                
                # Skip if in closed set or invalid
                if neighbor in closed_set or not self.is_valid_move(neighbor):
                    continue
                
                # Calculate tentative actual_score
                tentative_actual_score = actual_score[current] + self.move_cost(neighbor)
                
                # If this path is better than any previous one
                if tentative_actual_score < actual_score[neighbor]:
                    # Record this path
                    came_from[neighbor] = current
                    actual_score[neighbor] = tentative_actual_score
                    f_score[neighbor] = tentative_actual_score + self.heuristic(neighbor, goal)
                    
                    # Add to open set if not already there
                    if neighbor not in [pos for _, pos in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # No path found
    
    def get_available_directions(self, position):
        """Get available directions from a position"""
        # If this is the snake's head, use snake's available directions
        if position == self.snake.get_head_position():
            return self.snake.get_available_dire(self.snake.direction)
        
        # Otherwise return all four directions
        return [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT
    
    def is_valid_move(self, position):
        """Check if a move is valid (not a collision)"""
        # Check grid boundaries
        if not self.grid.is_valid_position(position):
            return False
        
        # Check collision with own body (except tail which will move)
        if position in self.snake.body[:-1]:
            return False
        
        # Check collision with opponent
        if position in self.snake.radar(self.opponent):
            return False
        
        return True
    
    def move_cost(self, position):
        """Calculate the cost/reward of moving to a position"""
        # Check for traps (penalty)
        for trap_pos, _ in self.food_manager.spike_trap_items:
            if position == trap_pos:
                return self.values['trap_cost']
        
        # Check for normal food (reward)
        for food_pos, _ in self.food_manager.normal_food_items:
            if position == food_pos:
                return self.values['normal_food_cost']  # Negative because A* minimizes cost
        
        # Check for super food (higher reward)
        for food_pos, _ in self.food_manager.super_food_items:
            if position == food_pos:
                return self.values['super_food_cost']  # Negative because A* minimizes cost
        
        # Normal move
        return self.values['normal_move_cost']  # Small reward for each step
    
    def heuristic(self, a, b):
        """Heuristic function for A* (Manhattan distance + penalties)"""
        # Base heuristic: Manhattan distance
        base_h = self.manhattan_distance(a, b)
        
        # Add penalties for dangerous areas
        penalty = 0
        
        # Penalty for being near opponent snake
        visible_segments = self.snake.radar(self.opponent)
        for segment in visible_segments:
            dist = self.manhattan_distance(a, segment)
            if dist <= 2:  # Close to opponent
                penalty += (3 - dist) * 10
        
        # Penalty for being near traps
        for trap_pos, _ in self.food_manager.spike_trap_items:
            dist = self.manhattan_distance(a, trap_pos)
            if dist <= 2:  # Close to trap
                penalty += (3 - dist) * 3
        
        return base_h + penalty
    
    def manhattan_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def reconstruct_path(self, came_from, current):
        """Reconstruct path from came_from dictionary"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        
        # Reverse to get path from start to goal
        path.reverse()
        return path
    
