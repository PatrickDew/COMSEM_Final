import pygame
import random
import math

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RADIUS = 20
SPEED = 3
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define Raven class
class Raven:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x < RADIUS or self.x > SCREEN_WIDTH - RADIUS:
            self.dx *= -1
        if self.y < RADIUS or self.y > SCREEN_HEIGHT - RADIUS:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (self.x, self.y), RADIUS)

# Define Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == "up":
            self.y -= SPEED
        elif direction == "down":
            self.y += SPEED
        elif direction == "left":
            self.x -= SPEED
        elif direction == "right":
            self.x += SPEED

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), RADIUS)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Raven Game")

# Create Raven objects
ravens = [Raven(random.randint(RADIUS, SCREEN_WIDTH - RADIUS), 
                random.randint(RADIUS, SCREEN_HEIGHT - RADIUS),
                random.randint(-SPEED, SPEED),
                random.randint(-SPEED, SPEED)) for _ in range(5)]

# Create Player object
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move("up")
    if keys[pygame.K_DOWN]:
        player.move("down")
    if keys[pygame.K_LEFT]:
        player.move("left")
    if keys[pygame.K_RIGHT]:
        player.move("right")

    screen.fill(WHITE)

    # Update and draw Ravens
    for raven in ravens:
        raven.update()
        raven.draw(screen)

    # Draw Player
    player.draw(screen)

    # Collision detection
    for raven in ravens:
        distance = math.sqrt((player.x - raven.x)**2 + (player.y - raven.y)**2)
        if distance < 2 * RADIUS:
            # Game over if player collides with a raven
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()