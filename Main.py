import pygame
import serial
import random


# Game variables
grape_score = 0
tomato_score = 0
orange_score = 0
score = 0
fruits = []
FRUIT_SIZE = 100
fruit_speed = 5
game_over = False;
max_fruit_in_screen = 8

fruits_name = [
    "Grape",
    "Tomato",
    "Orange"
]

fruit_map = {
    "G": "Grape",
    "T": "Tomato",
    "O": "Orange"
}


running = True

WIDTH, HEIGHT = 1360, 768


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Game")
clock = pygame.time.Clock()

game_Time = 60
timer = 0

start_tick = 0

# Serial Setup
#ser = serial.Serial('COM5', 115200, timeout=0.1)
#ser = serial.Serial("/dev/ttyAPE0",baudrate=115200,timeout=0.1)

# MainMenu
# SetUp
# Play
# GameOver
state = {
    "M": "MainMenu",
    "S": "SetUp",
    "P":"Play",
    "G":"GameOver"
}
game_state = state["M"]

# Iamge
fruit_image = {
    name: pygame.image.load(f"{name}.png").convert_alpha() for name in fruits_name
}
fruit_image_reScale = {
    name:pygame.transform.scale(image,(FRUIT_SIZE,FRUIT_SIZE)) for name,image in fruit_image.items()
}

    
fruit_image = fruit_image_reScale

fruit_hit_image = {
    name:pygame.image.load(f'{name}_Hit.png').convert_alpha() for name in fruits_name
}
back_ground = pygame.image.load("bg-gameplay.png")
back_ground = pygame.transform.scale(back_ground,(WIDTH,HEIGHT))

# Fruit Class
class Fruit:
    
    def __init__(self, x, y, speed,name,image,hit_image):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.speed = speed
        self.hit_image = hit_image
        self.is_hit = False
  
        
      
    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(self.image,(self.x,self.y))

    def Get_Y_Position(self):
        return self.y

    def Hit(self):
        self.is_hit = True
        global grape_score,tomato_score,tomato_score
        if self.name == "Grape":
            grape_score += 1
        elif self.name == "Tomato":
            tomato_score += 1
        elif self.name == "Orange":
            orange_score += 1
            
        screen.blit(self.hit_image,(self.x,self.y))


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
   
    x = random.randint(130, WIDTH - FRUIT_SIZE)
   
    name = random.choice(fruits_name)
    speed = random.choice([5,7,8])
    fruits.append(Fruit(x, 0,speed,name,fruit_image[name],fruit_hit_image[name]))


def Micro_Bit_Serial():
     if ser.in_waiting > 0:
        command = ser.readline().decode().strip()
        print(command)
        Check_Fruit(command)

def Input_Test(event):
   
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_g:
            Check_Fruit("G")
            
        if event.key == pygame.K_t:
            Check_Fruit("T")
                
        if event.key == pygame.K_o:
            Check_Fruit("O")

def Check_Fruit(input):
    print(fruit_map[input])
    global fruits,score
    global grape_score,tomato_score,tomato_score
    if len(fruits) == 0 : 
        return
   
    for fruit in fruits[:]:
       if fruit.name == fruit_map[input] and not fruit.is_hit:
           fruit.Hit()
           fruits.remove(fruit)
           #score += 1
           return
    name = random.choice(fruits_name)
    if name == "Grape":
        grape_score -= 1
    elif name == "Tomato":
        tomato_score -= 1
    elif name == "Orange":
        orange_score -= 1





def Update_Fruit():
    global fruits,hp
    for fruit in fruits[:]:
        fruit.fall()
        fruit.draw()    
        if fruit.Get_Y_Position() > HEIGHT:
            fruits.remove(fruit)
            #hp -= 1


def DisplayScore():
    #Grape
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"{grape_score}",True,BLACK)
    screen.blit(score_text,(WIDTH *0.085,HEIGHT * 0.18))
    
    #Tomato
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"{tomato_score}",True,BLACK)
    screen.blit(score_text,(WIDTH *0.085,HEIGHT * 0.50))
    
    #Orange
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"{orange_score}",True,BLACK)
    screen.blit(score_text,(WIDTH *0.085,HEIGHT * 0.83))

def DiaplayTime():
    font = pygame.font.SysFont(None,36)
    timer_text = font.render(f"Time: {timer}",True,BLACK)
    text_width,text_height = timer_text.get_size()
    screen.blit(timer_text,(WIDTH - text_width - 10,10))

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

    # if ser.in_waiting > 0:
    #     command = ser.readline().decode().strip()
    #     if command == "B":
    #         SetUpGame()



def SetUpGame():
    global hp,score,fruits,game_over
    rape_score = 0
    tomato_score = 0
    orange_score = 0
    fruits = []
    game_over = False
    start_tick = pygame.time.get_ticks()
    



def Change_State(new_state):
    global game_state
    game_state = new_state
    if game_state == state["M"]:
        pass
    elif game_state == state["S"]:
        
        SetUpGame()
        Change_State(state["P"])
        pass
    elif game_state == state["P"]:
        pass
    elif game_state == state["G"]:
        pass

Change_State(state["S"])
while running:
    if game_state == state["M"]:
        pass
    elif game_state == state["S"]:
        pass
    elif game_state == state["P"]:
        
        if not game_over :
        
        #BackGround
            screen.blit(back_ground,(0,0))
        # Create fruits
            Generate_Fruit()
       
        # Read Micro:bit input
        #Micro_Bit_Serial()

        # Update  fruits
            Update_Fruit()
        # Time
            elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
            timer = max(0,game_Time - int(elapsed_time))

            if timer <= 0:
                Change_State(state["G"])
       
        # Display UI
            DisplayScore()
            DiaplayTime()

        
            
    elif game_state == state["G"]:
        GameOver()
        pass
   


   

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                GameOver()
            if event.key == pygame.K_ESCAPE:
                running = False
        Input_Test(event)
    #print(len(fruits))
    #Update Screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
#ser.close()
