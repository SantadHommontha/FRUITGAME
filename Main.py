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
hp = 3
score = 0
fruits = []
FRUIT_SIZE = 100
fruit_speed = 5
game_over = False;
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
    if len(fruits) >= max_fruit_in_screen :
        return
    
    if len(fruits) == 0:
        Create_Fruit()
    

    else:
        if random.randint(0,30) == 1:
            Create_Fruit()
        
       
def Create_Fruit():
   
    x = random.randint(0, WIDTH - FRUIT_SIZE)
   
    name = random.choice(fruits_name)
    speed = random.choice([5,7,8])
    fruits.append(Fruit(x, 0,speed,name,fruit_image[name]))


def Micro_Bit_Serial():
     if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(command)
        Check_Fruit(command)
      

def Check_Fruit(input):
    global fruits,score
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
    global fruits,hp
    for fruit in fruits[:]:
        fruit.fall()
        fruit.draw()    
        if fruit.Get_Y_Position() > HEIGHT:
            fruits.remove(fruit)
            hp -= 1


def DisplayScore():
    
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}",True,BLACK)
    screen.blit(score_text,(10,10))

def DiaplayHP():
    font = pygame.font.SysFont(None,36)
    hp_text = font.render(f"HP: {hp}",True,BLACK)
    text_width,text_height = hp_text.get_size()
    screen.blit(hp_text,(WIDTH - text_width - 10,10))

def GameOver():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 100)
    gameOver = font.render(f"Game Over",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 5))

    font = pygame.font.SysFont(None, 60)
    gameOver = font.render(f"Score: {score}",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 3))


    font = pygame.font.SysFont(None, 50)
    gameOver = font.render("Touch Banana To Play Again",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 2))

    if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        if command == "B":
            SetUpGame()



def SetUpGame():
    global hp,score,fruits,game_over
    hp = 3
    score = 0
    fruits = []
    game_over = False


running = True
while running:
    if not game_over :
        screen.fill(WHITE)

        # Create fruits
        Generate_Fruit()

        # Read Micro:bit input
        Micro_Bit_Serial()

        # Update  fruits
        Update_Fruit()
       

        # Display UI
        DisplayScore()
        DiaplayHP()

    else:
        GameOver()


    # Chack HP
    if hp <= 0:
        game_over = True

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                GameOver()

    #Update Screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
ser.close()
