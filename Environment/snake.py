import pygame
from environment_constants import *


class Snake:
    def __init__(self, position, color, name):
        self.body = [position]  # Start with just the head
        self.color = color
        self.name = name
        self.direction = (0, 0)  # Initially not moving
        self.score = 0
        self.segments_to_add = 0 # to add new segment

    def set_direction(self, direction):
        """Set the snake's direction"""
        # Prevent moving in the opposite direction
        self.direction = direction


    def get_direction(self, current_direction):
        """Give available direction"""
        directions = [(0,-1),(0,1),(-1,0),(1,0)]
        available_directions = []
        current_x, current_y = current_direction

        for direction in directions:
            x, y = direction
            if not ((x == -current_x and y == -current_y) and len(self.body) != 1):
                available_directions.append(direction)

        return available_directions

    def update_move(self, movement):
        """Update the snake's position"""
        # Get the current head position
        head_x, head_y = self.body[0]

        self.set_direction(movement)
        # Calculate new head position
        direction_x, direction_y = self.direction
        new_head = (head_x + direction_x, head_y + direction_y)

        # Insert new head at the beginning of the body
        self.body.insert(0, new_head)

        # Add segments if needed
        if self.segments_to_add > 0:
            self.segments_to_add -= 1
        else:
            # Remove the tail if no segments to add
            self.body.pop()

    def grow(self, amount=1):
        """Add segments to the snake"""
        self.segments_to_add += amount

    def reduce_length(self):
        """Reduce the snake's length (for spike trap)"""
        if len(self.body) > 1:
            self.body.pop()  # Remove the tail
            return True

        return False # this will be used to end the game

    def get_head_position(self):
        """Get the position of the snake's head"""
        return self.body[0]

    def check_self_collision(self):
        """Check if the snake has collided with itself"""
        head = self.body[0]
        return head in self.body[1:]

    def radar(self, opponent):
        """Check if this snake can see the opponent within visibility range"""
        head_x, head_y = self.body[0]
        visible_segments = []

        # Check each opponent segment
        for segment in opponent.body:
            segment_x, segment_y = segment

            # Check if segment is within visibility range
            if (abs(segment_x - head_x) <= VISIBILITY_RANGE and
                    abs(segment_y - head_y) <= VISIBILITY_RANGE):
                visible_segments.append(segment)

        return visible_segments
#--------------------------------------------------------------
    def draw(self, screen):
        """Draw the snake on the screen"""
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * CELL_SIZE,
                segment[1] * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Draw rounded rect for the snake segment
            pygame.draw.rect(screen, self.color, rect, 0, 5)

            # Draw a darker outline
            pygame.draw.rect(screen, (0, 0, 0), rect, 1, 5)

        # Draw eyes on the head if snake has direction
        if self.direction != (0, 0) and len(self.body) > 0:
            head_x, head_y = self.body[0]
            head_rect = pygame.Rect(
                head_x * CELL_SIZE,
                head_y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            # Calculate eye positions based on direction
            eye_radius = CELL_SIZE // 8
            eye_offset = CELL_SIZE // 4

            # Default eye positions (facing right)
            left_eye_x = head_x * CELL_SIZE + CELL_SIZE - eye_offset
            left_eye_y = head_y * CELL_SIZE + eye_offset
            right_eye_x = head_x * CELL_SIZE + CELL_SIZE - eye_offset
            right_eye_y = head_y * CELL_SIZE + CELL_SIZE - eye_offset

            # Adjust eye positions based on direction
            if self.direction == UP:
                left_eye_x = head_x * CELL_SIZE + eye_offset
                left_eye_y = head_y * CELL_SIZE + eye_offset
                right_eye_x = head_x * CELL_SIZE + CELL_SIZE - eye_offset
                right_eye_y = head_y * CELL_SIZE + eye_offset
            elif self.direction == DOWN:
                left_eye_x = head_x * CELL_SIZE + eye_offset
                left_eye_y = head_y * CELL_SIZE + CELL_SIZE - eye_offset
                right_eye_x = head_x * CELL_SIZE + CELL_SIZE - eye_offset
                right_eye_y = head_y * CELL_SIZE + CELL_SIZE - eye_offset
            elif self.direction == LEFT:
                left_eye_x = head_x * CELL_SIZE + eye_offset
                left_eye_y = head_y * CELL_SIZE + eye_offset
                right_eye_x = head_x * CELL_SIZE + eye_offset
                right_eye_y = head_y * CELL_SIZE + CELL_SIZE - eye_offset

            # Draw the eyes
            pygame.draw.circle(screen, (255, 255, 255), (left_eye_x, left_eye_y), eye_radius)
            pygame.draw.circle(screen, (255, 255, 255), (right_eye_x, right_eye_y), eye_radius)

            # Draw pupils
            pygame.draw.circle(screen, (0, 0, 0), (left_eye_x, left_eye_y), eye_radius // 2)
            pygame.draw.circle(screen, (0, 0, 0), (right_eye_x, right_eye_y), eye_radius // 2)
