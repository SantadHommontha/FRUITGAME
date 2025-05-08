import pygame
import serial
import random

# Initialize
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

# Serial Setup
ser = serial.Serial('COM5', 115200, timeout=0.1)

# Game variables
score = 0
fruits = []
FRUIT_SIZE = 50
fruit_speed = 5
max_fruit_in_screen = 18


# Iamge


# Fruit Class
class Fruit:
  
    def __init__(self, x, y, color,speed,size):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.speed = speed
        self.size = size

    def fall(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x,self.y,self.size,self.size))

    def Get_Y_Position(self):
        return self.rect.y


# Function
def Generate_Fruit():
    global fruits
    if len(fruits) >= max_fruit_in_screen :
        return
    
    if len(fruits) == 0:
        Create_Fruit()
    

    if random.randint(0,30) == 1:
        Create_Fruit()
        
       
def Create_Fruit():
    global RED,YELLOW,ORANGE
    global WIDTH,FRUIT_SIZE
    x = random.randint(0, WIDTH - FRUIT_SIZE)
    color = random.choice([RED, YELLOW, ORANGE])
    speed = random.choice([5,7,8])
    fruits.append(Fruit(x, 0, color,speed,FRUIT_SIZE))


def Micro_Bit_Serial():
     if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(command)
        Check_Fruit(command)
      

def Check_Fruit(input):
    global RED,YELLOW,ORANGE,fruits,score
    if len(fruits) == 0 : 
        return

    fruit_map = {
        "B": YELLOW,
        "A": RED,
        "O": ORANGE
    }

    
    
    for fruit in fruits[:]:
       if fruit.color == fruit_map[input]:
           fruits.remove(fruit)
           score += 1
           return
    score -= 1





def Update_Fruit():
    global fruits,HEIGHT
    for fruit in fruits[:]:
        fruit.fall()
        fruit.draw()    
        if fruit.Get_Y_Position() > HEIGHT:
            fruits.remove(fruit)
# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Create fruits
    Generate_Fruit()

    # Read Micro:bit input
    Micro_Bit_Serial()

    # Update  fruits
    Update_Fruit()
       

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
