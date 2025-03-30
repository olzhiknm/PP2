import pygame, random

pygame.init()
WIDTH, HEIGHT = 600, 400
TILE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Disappearing Food")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BG = (0, 0, 0)

snake = [(100, 100), (90, 100), (80, 100)]
direction = (TILE, 0)
food = None

score = 0
level = 1
speed = 10


food_timer = 0
food_lifetime = 3000  

def generate_food():
    while True:
        x = random.randint(0, (WIDTH - TILE) // TILE) * TILE
        y = random.randint(0, (HEIGHT - TILE) // TILE) * TILE
        if (x, y) not in snake:
            return (x, y)

food = generate_food()
food_timer = pygame.time.get_ticks()

running = True
while running:
    screen.fill(BG)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, TILE):
        direction = (0, -TILE)
    elif keys[pygame.K_DOWN] and direction != (0, -TILE):
        direction = (0, TILE)
    elif keys[pygame.K_LEFT] and direction != (TILE, 0):
        direction = (-TILE, 0)
    elif keys[pygame.K_RIGHT] and direction != (-TILE, 0):
        direction = (TILE, 0)

    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    if (head[0] < 0 or head[0] >= WIDTH or
        head[1] < 0 or head[1] >= HEIGHT or
        head in snake):
        running = False

    snake.insert(0, head)

  
    if head == food:
        score += 1
        if score % 4 == 0:
            level += 1
            speed += 2
        food = generate_food()
        food_timer = pygame.time.get_ticks() 
    else:
        snake.pop()

    if pygame.time.get_ticks() - food_timer > food_lifetime:
        food = generate_food()
        food_timer = pygame.time.get_ticks() 

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, TILE, TILE))

    pygame.draw.rect(screen, RED, (*food, TILE, TILE))


    score_text = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
