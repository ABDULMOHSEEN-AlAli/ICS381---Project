import pygame
import sys
from game_logic import Game

def main():
    # Initialize pygame
    pygame.init()

    # Create game instance
    game = Game()

    # Main game loop
    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        # Update game state
        game.update()

        # Render frame
        game.render()

        # Cap the frame rate
        clock.tick(10)  # 15 frames per second matches the snake speed from your proposal
    print("Agent 1 takes:",game.snake1.get_total_time(),"ms, and Agent 2 takes: ", game.snake2.get_total_time()," ms")
    print("Total steps is :", game.turn_count)
    # Cleanup and exit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
