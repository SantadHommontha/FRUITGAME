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
FRUIT_SIZE = 100
fruit_speed = 5
max_fruit_in_screen = 8

fruits_name = [
    "Banana",
    "Apple",
    "Orange"
]
# Iamge
fruit_image = {
    name: pygame.image.load(f"{name}.png").convert_alpha() for name in fruits_name
}
fruit_image_reScale = {
    name:pygame.transform.scale(image,(FRUIT_SIZE,FRUIT_SIZE)) for name,image in fruit_image.items()
}

    
fruit_image = fruit_image_reScale
# Fruit Class
class Fruit:
    
    def __init__(self, x, y, speed,name,image):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        #self.rect = pygame.Rect(x, y, size, size)

       
        self.speed = speed
      

    def fall(self):
        self.y += self.speed

    def draw(self):
        #pygame.draw.rect(screen, self.color, pygame.Rect(self.x,self.y,self.size,self.size))
        screen.blit(self.image,(self.x,self.y))

    def Get_Y_Position(self):
        return self.y


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
    #global RED,YELLOW,ORANGE
    global WIDTH,fruit_image,fruits_name
    x = random.randint(0, WIDTH - FRUIT_SIZE)
    #color = random.choice([RED, YELLOW, ORANGE])
    name = random.choice(fruits_name)
    speed = random.choice([5,7,8])
    fruits.append(Fruit(x, 0,speed,name,fruit_image[name]))


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
        "B": "Banana",
        "A": "Apple",
        "O": "Orange"
    }

    
    
    for fruit in fruits[:]:
       if fruit.name == fruit_map[input]:
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


def DisplayScore():
    global score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}",True,BLACK)
    screen.blit(score_text,(10,10))
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
    # font = pygame.font.SysFont(None, 36)
    # score_text = font.render(f"Score: {score}", True, BLACK)
    # screen.blit(score_text, (10, 10))
    DisplayScore()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
ser.close()
