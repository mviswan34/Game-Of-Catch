import pygame
import random

# Constants
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 400
CELL_SIZE = 100
PLAYER_SPEED = CELL_SIZE
FRUIT_DROP_SPEED = CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Initialize pygame
pygame.init()

# Load images
player_image = pygame.image.load("C:/Users/megha/A Thesis/Flappy Bird/Game_Of_catch/basket.png")  # Replace with your image path
player_image = pygame.transform.scale(player_image, (100, 90))

fruit_image = pygame.image.load("C:/Users/megha/A Thesis/Flappy Bird/Game_Of_catch/fruit.png")     # Replace with your image path
fruit_image = pygame.transform.scale(fruit_image, (80, 80))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Falling Fruit')
BLACK = (0, 0, 0)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

class Player:
    def __init__(self):
        self.x = 0
        self.y = SCREEN_HEIGHT - CELL_SIZE

    def move(self, direction):
        new_x = self.x + direction * CELL_SIZE
        if 0 <= new_x < SCREEN_WIDTH:
            self.x = new_x

    def draw(self):
        screen.blit(player_image, (self.x, self.y))

class Fruit:
    def __init__(self, x):
        self.x = x
        self.y = 0

    def move(self):
        self.y += FRUIT_DROP_SPEED/FPS

    def draw(self):
        screen.blit(fruit_image, (self.x, self.y))

    def is_caught(self, player):
        return self.y == player.y and self.x == player.x

    def is_missed(self):
        return self.y > SCREEN_HEIGHT
    
    def remove(self):
        screen.blit(fruit_image, (self.x, self.y))

player = Player()
fruits = []
score = 0

FPS = 30
fruit_drop_interval = FPS  # 30 frames, which means the fruit will drop once every second
fruit_drop_counter = 0

FRUIT_DROP_SPEED = CELL_SIZE

running = True
while running:
    screen.fill(WHITE)
    draw_grid()
    fruit_drop_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move(-1)
                score -= 0.1
            elif event.key == pygame.K_RIGHT:
                player.move(1)
                score -= 0.1

    # Randomly spawn a fruit
    if random.random() < 0.02:  # 2% chance per frame to spawn a fruit
        x = random.choice([i * CELL_SIZE for i in range(4)])
        fruits.append(Fruit(x))

    # Check if it's time to move the fruits
    if fruit_drop_counter >= fruit_drop_interval:
        for fruit in fruits:
            fruit.move()
        fruit_drop_counter = 0

    # Move and draw fruits
    for fruit in fruits[:]:
        fruit.move()
        fruit.draw()

        if fruit.is_caught(player):
            score += 10
            fruit.remove(fruit)
        elif fruit.is_missed():
            score -= 10
            fruit.remove(fruit)

    player.draw()

    # Show score
    score_display = pygame.font.Font(None, 36).render(str(score), True, GREEN)
    screen.blit(score_display, (10, 10))

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

pygame.quit()
