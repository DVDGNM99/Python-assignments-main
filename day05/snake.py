import pygame              # Import the pygame library for game development
import random              # Import random for generating random positions for food

# settings
WIDTH, HEIGHT = 400, 400   # Set the width and height of the game window
CELL = 20                  # Define the size of each grid cell for movement

pygame.init()              # Initialize all pygame modules
win = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window with the given size
clock = pygame.time.Clock()                    # Create a clock to control the game framerate

# position 
snake = [(100, 100)]       # Initialize the snake as a list with one segment at position (100,100)
dx, dy = CELL, 0           # Set initial movement direction (moving right by CELL pixels)
food = (200, 200)          # Set the starting position of the food

def new_food():
    return (random.randrange(0, WIDTH, CELL),   # Generate a random x-position aligned to the grid
            random.randrange(0, HEIGHT, CELL))  # Generate a random y-position aligned to the grid

running = True             # Control variable for the game loop
while running:             # Start the main game loop
    pygame.time.delay(80)  # Add a small delay to control game speed
    for event in pygame.event.get():           # Process all incoming events
        if event.type == pygame.QUIT:          # Check if the window was closed
            running = False                    # Stop the game loop
        # direction control
        if event.type == pygame.KEYDOWN:       # Check if a key was pressed
            if event.key == pygame.K_UP and dy == 0:      # Move up only if not already moving vertically
                dx, dy = 0, -CELL                          # Change direction to upward
            elif event.key == pygame.K_DOWN and dy == 0:  # Move down only if not already moving vertically
                dx, dy = 0, CELL                           # Change direction to downward
            elif event.key == pygame.K_LEFT and dx == 0:  # Move left only if not already moving horizontally
                dx, dy = -CELL, 0                          # Change direction to left
            elif event.key == pygame.K_RIGHT and dx == 0: # Move right only if not already moving horizontally
                dx, dy = CELL, 0                           # Change direction to right

    # move snake
    head = (snake[0][0] + dx, snake[0][1] + dy)   # Compute the new head position based on movement direction
    snake.insert(0, head)                         # Insert the new head at the beginning of the snake list

    # eat food
    if head == food:           # Check if the snake head reached the food
        food = new_food()      # Generate new food at a random location
    else:
        snake.pop()            # Remove the last segment to keep the snake the same length

    # collision
    if (head[0] < 0 or head[0] >= WIDTH or         # Check collision with left or right borders
        head[1] < 0 or head[1] >= HEIGHT or        # Check collision with top or bottom borders
        head in snake[1:]):                        # Check collision with its own body
        running = False                            # End the game loop if a collision occurs

    # draw everything
    win.fill((0, 0, 0))                            # Clear the screen by filling it with black
    for x, y in snake:                             # Iterate through all snake segments
        pygame.draw.rect(win, (0, 255, 0), (x, y, CELL, CELL))  # Draw each segment as a green square
    pygame.draw.rect(win, (255, 0, 0), (food[0], food[1], CELL, CELL))  # Draw the food as a red square

    pygame.display.update()                        # Update the screen with the new drawings
    clock.tick(10)                                 # Limit the game to 10 frames per second

pygame.quit()                                      # Quit pygame and close the window
