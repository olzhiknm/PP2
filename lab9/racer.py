import pygame, random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Weighted Coins")

WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

car_img = pygame.image.load("player.png")
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = car_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 70)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 3, 5]) 
        self.image = coin_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, WIDTH - 30), -30)

    def update(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > HEIGHT:
            self.kill()

player = Player()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

score = 0
COIN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_EVENT, 1000)

running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == COIN_EVENT:
            coin = Coin()
            coins.add(coin)
            all_sprites.add(coin)

    all_sprites.update()

    collected = pygame.sprite.spritecollide(player, coins, True)
    for coin in collected:
        score += coin.weight


    all_sprites.draw(screen)
    score_text = font.render(f"Coins: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
