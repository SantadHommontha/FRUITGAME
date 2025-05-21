import pygame
import serial
import random

pygame.init()
#Serial Setup
ser = None
try:
    #Fild Port in Windows use commmad mode in termianl and rasberry pi use ls /dev/tty* in ternimal
    #In wiodow micro:bit port name Often named COM5 and rasberry pi /dev/ttyACM0
    #Or Uncomment below for windows or rasberray pi
    #ser = serial.Serial(port='COM5', baudrate=115200, timeout=0.1) # Windows
    ser = serial.Serial(port="/dev/ttyAPE0",baudrate=115200,timeout=0.1) # raspberry pi
    print("Found Micro:Bit")
except:
     print("Not Found Micro:bit")
# Game variables
grape_score = 0
tomato_score = 0
orange_score = 0
mistake_score = 0
is_fullScreen = True
running = True
# Game Screen Size
WIDTH, HEIGHT = 1360, 768

# Time
game_Time = 10
timer = 0
start_tick = 0 

# Font
font_path = "CherryBombOne-Regular.ttf"
font_small = pygame.font.Font(font_path,36) # small font
font_medium = pygame.font.Font(font_path,60) # medium font
font_large = pygame.font.Font(font_path,100) # large font

# Fruit Properties
spawn_rate  = 30 
max_fruit_in_screen = 10 # quantity of fruit at create on screen
fruits = [] 
fruit_speed = [5,10,15]
FRUIT_SIZE = 100

# Fruit Name
fruits_name = [
    "Grape",
    "Tomato",
    "Orange"
]

#Used to check the values ​​sent from Microbit.
fruit_map = {
    "G": "Grape",
    "T": "Tomato",
    "O": "Orange"
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Initialize
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Game")
clock = pygame.time.Clock()


# Iamge
# Load Fruit Image
fruit_image = {
    name: pygame.image.load(f"{name}.png").convert_alpha() for name in fruits_name
}
# Change Fruit Scale
fruit_image_reScale = {
    name:pygame.transform.scale(image,(FRUIT_SIZE,FRUIT_SIZE)) for name,image in fruit_image.items()
}

fruit_image = fruit_image_reScale

# Load Fruit Hit Image
fruit_hit_image = {
    name:pygame.image.load(f'{name}_Hit.png').convert_alpha() for name in fruits_name
}
# Change Fruit Hit Scale
fruit_hit_image_reScale = {
    name:pygame.transform.scale(image,(FRUIT_SIZE,FRUIT_SIZE)) for name,image in fruit_hit_image.items()
}

fruit_hit_image = fruit_hit_image_reScale

# Load Menu background Image
menu_background = pygame.image.load("bg-startscene.png").convert_alpha()
menu_background = pygame.transform.scale(menu_background,(WIDTH,HEIGHT))


# Load play background Image
back_ground = pygame.image.load("bg-gameplay.png")
back_ground = pygame.transform.scale(back_ground,(WIDTH,HEIGHT))

# Game State
state = {
    "M": "MainMenu",
    "S": "SetUp",
    "P":"Play",
    "G":"GameOver"
}
game_state = state["M"]

    
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
        self.is_dead = False
        
    def fall(self):
        self.y += self.speed

    def draw(self):
        if(self.is_hit):
            self.elapsed_time = (pygame.time.get_ticks() - self.start_tick) / 1000
            self.timer = (0.2 - self.elapsed_time)
            if self.timer <= 0:
                self.is_dead = True
            screen.blit(self.hit_image,(self.x,self.y))
        else:
            screen.blit(self.image,(self.x,self.y))

    def Get_Y_Position(self):
        return self.y

    def Hit(self):
        self.is_hit = True
        
        global grape_score,tomato_score,orange_score
        if self.name == "Grape":
            grape_score += 1
        elif self.name == "Tomato":
            tomato_score += 1
        elif self.name == "Orange":
            orange_score += 1
        self.start_tick = pygame.time.get_ticks()
       


# Function
def Toggle_FullScreen():
    global is_fullScreen,screen
    
    if is_fullScreen:
        screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH,HEIGHT))

    is_fullScreen = not is_fullScreen

def Generate_Fruit():
    if len(fruits) >= max_fruit_in_screen :
        return
    
    if len(fruits) == 0:
        Create_Fruit()
    else:
        if random.randint(1,spawn_rate ) == 1:
            Create_Fruit()
        
       
def Create_Fruit():
   
    x = random.randint(130, WIDTH - FRUIT_SIZE)
   
    name = random.choice(fruits_name)
    speed = random.choice(fruit_speed)
    fruits.append(Fruit(x, 0,speed,name,fruit_image[name],fruit_hit_image[name]))

# Read values Form MicroBit
def Micro_Bit_Serial():
    # if not found MicroBit this Function will Return
    if not ser :
        return
    if game_state == state["M"]:
         if ser.in_waiting > 0:
            microBit_text = ser.readline().decode().strip()
            if microBit_text in fruit_map:
                Change_State(state["S"])
    elif game_state == state["P"]:
        if ser.in_waiting > 0:
            microBit_text = ser.readline().decode().strip()
            print(microBit_text)
            Check_Fruit(microBit_text)
    elif game_state == state["G"]:
        if ser.in_waiting > 0:
            microBit_text = ser.readline().decode().strip()
            if microBit_text in fruit_map:
                Change_State(state["S"])
# Test Game With Keyboard
def Input_Test(event):  
    if game_state == state["M"]:
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g or event.key == pygame.K_t or  event.key == pygame.K_o:
              Change_State(state["S"])
    elif game_state == state["P"]:
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                Check_Fruit("G")
            if event.key == pygame.K_t:
                Check_Fruit("T")     
            if event.key == pygame.K_o:
                Check_Fruit("O")
    elif game_state == state["G"]:
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g or event.key == pygame.K_t or  event.key == pygame.K_o:
              Change_State(state["S"])

def Check_Fruit(input):
    global fruits , mistake_score
    if len(fruits) == 0 : 
        return
    for fruit in fruits[:]:
        if fruit.name == fruit_map[input] and not fruit.is_hit:
            
            fruit.Hit()
            return
    mistake_score += 1





def Update_Fruit():
    global fruits,hp
    for fruit in fruits[:]:
        fruit.fall()
        fruit.draw()    
        if fruit.Get_Y_Position() > HEIGHT and not fruit.is_dead:
            fruits.remove(fruit)
        if fruit.is_dead:
            fruits.remove(fruit)


def DisplayScore():
    #Grape
    score_text = font_small.render(f"{grape_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.19)
    screen.blit(score_text,score_rect)
    
    #Tomato
    score_text = font_small.render(f"{tomato_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.52)
    screen.blit(score_text,score_rect)
    
    #Orange
    score_text = font_small.render(f"{orange_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.84)
    screen.blit(score_text,score_rect)

def DiaplayTime():
    timer_text = font_medium.render(f"{timer}",True,BLACK)
    timer_rect = timer_text.get_rect()
    timer_rect.center = (WIDTH  - 150,80)
    screen.blit(timer_text,timer_rect)

def GameOver():
    screen.fill(BLACK)
  
    gameOver = font_large.render(f"Game Over",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 5))

    gameOver = font_medium.render(f"Score Sum: {(grape_score + tomato_score + orange_score) - mistake_score}",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 3))
    
    if timer <= 0:
        gameOver = font_medium.render("Touch Any Fruit To Play Again",True,WHITE)
        text_width, text_height = gameOver.get_size()
        screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 2))




def SetUpGame():
    global hp,grape_score,tomato_score,orange_score,fruits,start_tick,mistake_score
    mistake_score = 0
    grape_score = 0
    tomato_score = 0
    orange_score = 0
    fruits = []
    start_tick = pygame.time.get_ticks()
    
def Change_State(new_state):
    global game_state
    global timer,start_tick
    print(f"New {new_state}")
    game_state = new_state
    if game_state == state["M"]:
        screen.blit(menu_background,(0,0))
    elif game_state == state["S"]:
        SetUpGame()
        Change_State(state["P"])
        pass
    elif game_state == state["P"]:
        pass
    elif game_state == state["G"]:
        timer = 0
        start_tick = pygame.time.get_ticks()
        

Change_State(state["M"])
#Toggle_FullScreen()

# Main Loop
while running:
     # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_f:
                Toggle_FullScreen()
            
        if game_state == state["M"]:
            Input_Test(event)
        elif game_state == state["S"]:
            pass
        elif game_state == state["P"]:
            Input_Test(event)
            
        elif game_state == state["G"]:
            if(timer <= 0):
                Input_Test(event)
            
        
    
    if game_state == state["M"]:
       screen.blit(menu_background,(0,0))
       # Read Micro:bit serial
       Micro_Bit_Serial()
       
    elif game_state == state["S"]:
        pass
    elif game_state == state["P"]:
        
        # BackGround
        screen.blit(back_ground,(0,0))    
        # Create fruits
        Generate_Fruit()
        # Read Micro:bit serial
        Micro_Bit_Serial()
        # Update  fruits
        Update_Fruit()
        
        # Timer
        elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
        timer = max(0,game_Time - int(elapsed_time))

        if timer <= 0:
            Change_State(state["G"]) 
        # Display UI
        DisplayScore()
        DiaplayTime()
        
    elif game_state == state["G"]:
        GameOver()
        elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
        timer = max(0,1.5 - int(elapsed_time))
        if(timer <= 0):
            Micro_Bit_Serial()
        
       
        
    #Update Screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
