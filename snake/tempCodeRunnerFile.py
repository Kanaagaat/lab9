import pygame
import random


pygame.init()
# Define cell size and grid dimensions (20x20)
cell_size = 40
cell_number = 20
clock = pygame.time.Clock()
done = False
score = 0


# Colors
color_red = (255, 0, 0)         # 1 очко
color_purple = (128, 0, 128)    # 2 очка
color_orange = (255, 68, 51)    # 3 очка
color_green = (0,255,0)
color_white = (255,255,255)

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Variables for movement
x_pos = 0
y_pos = 0
# Fruit position
x_f = 0
y_f = 0
# Snake's initial position
x_ch = (cell_number // 2) * cell_size
y_ch = (cell_number // 2) * cell_size


length = 2
snake_lst = [[x_ch, y_ch]]
direction = "UP"
fps = 5
level = 1

fruit_types = [
    (color_red, 1),     # Красный фрукт - 1 очко
    (color_purple, 2),  # Фиолетовый фрукт - 2 очка
    (color_orange, 3)   # Оранжевый фрукт - 3 очка
]
fruit_spawn_time = 5000 # interval time between fruits appearence
last_fruit_time = pygame.time.get_ticks()  # last appearence of fruits

# Function to check if the game is over
def game_over(x, y):
    if x < 0 or x >= cell_number * cell_size or y < 0 or y >= cell_number * cell_size:
        return True
    return False
# Function to generate a new fruit position
def fruit():
    while True:
        x = random.randint(0, cell_number - 1) * cell_size
        y = random.randint(0, cell_number - 1) * cell_size
        if [x, y] not in snake_lst:
            if level < 3:
                return x, y, (color_red, 1)  # static coclor until 3 level
            return x, y, random.choice(fruit_types)  # after 3 level randomly

# Generate the first fruit position            
x_f, y_f, fruit_info = fruit()

# Function to draw the snake on the screen
def draw_snake():
    for x in snake_lst:
        pygame.draw.rect(screen, color_green, (x[0], x[1], cell_size, cell_size))



while not done:
   
    pygame.display.set_caption(f"Score: {score} Level: {level}")
    screen.fill(color_white)
    # Increase game difficulty based on the score
    if score > 5:
        score = 0
        level += 1
        fps += 5

    current_time = pygame.time.get_ticks()
    if current_time - last_fruit_time >= fruit_spawn_time: # check fruit appearnce
        x_f, y_f, fruit_info = fruit() # new fruit
        last_fruit_time = current_time #change last fruit appearence time


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"

  # Update movement direction based on user input    
    if direction == "UP":
        y_pos = -cell_size
        x_pos = 0
    elif direction == "DOWN":
        y_pos = cell_size
        x_pos = 0
    elif direction == "RIGHT":
        x_pos = cell_size
        y_pos = 0
    elif direction == "LEFT":
        x_pos = -cell_size
        y_pos = 0



    # Move the snake's head
    x_ch += x_pos
    y_ch += y_pos
    
    if game_over(x_ch, y_ch) or [x_ch, y_ch] in snake_lst:
        screen.fill(color_white)
        message = font.render("GAME OVER", True, color_red)
        message_rect = message.get_rect(center=((cell_number * cell_size) // 2, (cell_number * cell_size) // 2))
        screen.blit(message, message_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  
        done = True
        break  

    # Update snake's body by adding the new head position
    snake_lst.append([x_ch, y_ch])
    # Keep the snake's length correct by removing the oldest segment
    if len(snake_lst) > length:
        del snake_lst[0]
                
    random_increase_fruit =  1           
# Check if the snake has eaten the fruit
    if x_ch == x_f and y_ch == y_f:
        last_fruit_time = current_time
        if level >= 3: # after third level  length of the snake will increase randomly by 1 or 2 or 3
            score += fruit_info[1]  # Прибавляем очки фрукта
            length += fruit_info[1]  # Увеличиваем длину на значение фрукта
            x_f, y_f, fruit_info = fruit()
        else:
            score += 1
            length += 1
            x_f, y_f, fruit_info = fruit() 

    pygame.draw.rect(screen, fruit_info[0], (x_f, y_f, cell_size, cell_size))




    draw_snake()
   






            
            





    clock.tick(fps)
    pygame.display.flip()


        
pygame.quit()
