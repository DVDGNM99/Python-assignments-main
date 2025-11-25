import pygame
import random

# --- impostazioni di base ---
WIDTH, HEIGHT = 400, 400
CELL = 20

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# posizione iniziale del serpente
snake = [(100, 100)]
dx, dy = CELL, 0  # movimento iniziale verso destra
food = (200, 200)

def new_food():
    return (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

running = True
while running:
    pygame.time.delay(80)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # controllo direzione
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0

    # muovi il serpente
    head = (snake[0][0] + dx, snake[0][1] + dy)
    snake.insert(0, head)

    # mangia il cibo
    if head == food:
        food = new_food()
    else:
        snake.pop()

    # collisioni
    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        head in snake[1:]):
        running = False

    # disegna tutto
    win.fill((0, 0, 0))
    for x, y in snake:
        pygame.draw.rect(win, (0, 255, 0), (x, y, CELL, CELL))
    pygame.draw.rect(win, (255, 0, 0), (food[0], food[1], CELL, CELL))

    pygame.display.update()
    clock.tick(10)

pygame.quit()
