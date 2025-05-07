import pygame
import serial
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Defender")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Serial Setup (Adjust COM port as needed)
ser = serial.Serial('COM5', 115200, timeout=1)

# Game variables
score = 0
fruits = []
FRUIT_SIZE = 50
fruit_speed = 5

class Fruit:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, FRUIT_SIZE, FRUIT_SIZE)
        self.color = color

    def fall(self):
        self.rect.y += fruit_speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Generate new fruits
    if random.randint(1, 50) == 1:
        x = random.randint(0, WIDTH - FRUIT_SIZE)
        color = random.choice([RED, YELLOW])
        fruits.append(Fruit(x, 0, color))

    # Read Micro:bit input
    if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(command)
        for fruit in fruits[:]:
            if command == 'O' and fruit.color == ORANGE:
                fruits.remove(fruit)
                score += 1
            elif command == 'B' and fruit.color == YELLOW:
                fruits.remove(fruit)
                score += 1
            elif command == 'A' and fruit.color == RED:
                fruits.remove(fruit)
               
                score += 1

    # Update and draw fruits
    for fruit in fruits[:]:
        fruit.fall()
        fruit.draw()
        #if fruit.rect.y > HEIGHT:
            #running = False  # Game over

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
ser.close()
