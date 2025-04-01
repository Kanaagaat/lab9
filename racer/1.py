import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()

cell_size = 30
cell_number = 20
Score = 0
Level = 1
coin_score = 0

# COLORS
Red = (255, 0, 0)
White = (255, 255, 255)

# Player class
class Player:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.im = pygame.image.load("PygameTutorial_3_0/Player.png")
        self.im = pygame.transform.scale(self.im, (70,100))
    
    def image(self):
        return self.im.get_rect(center=(self.x, self.y))

# Enemy class
class Enemy:
    def __init__(self, x_pos, y_pos, speed):
        self.im = pygame.image.load("PygameTutorial_3_0/Enemy.png")
        self.x = x_pos
        self.y = y_pos
        self.speed = speed

    def image(self):
        return self.im.get_rect(midbottom=(self.x, self.y))

# Coin class
class Coin:
    def __init__(self, x_pos, y_pos, speed, path, value):
        self.im = pygame.image.load(path)
        self.im = pygame.transform.scale(self.im, (50,50))
        self.x = x_pos
        self.y = y_pos
        self.speed = speed
        self.value = value

    def image(self):
        return self.im.get_rect(midbottom=(self.x, self.y))

# Setting screen size
screen = pygame.display.set_mode((cell_size * cell_number, cell_number * cell_size))

font = pygame.font.Font("font/Pixeltype.ttf", 50)
message = font.render("GAME OVER", True, Red)
message_rect = message.get_rect(center=((cell_number * cell_size) // 2, (cell_number * cell_size) // 2))

bg = pygame.image.load("PygameTutorial_3_0/AnimatedStreet.png")
bg = pygame.transform.scale(bg, (cell_size * cell_number, cell_number * cell_size))
bg_rect = bg.get_rect(topleft=(0, 0))

# Background music
musics = [
    "PygameTutorial_3_0/background.wav",
    "PygameTutorial_3_0/crash.wav"
]

pygame.mixer.music.load(musics[0])
pygame.mixer.music.play(-1)

# Coin types 
coin_types = [
    ("racer/dollar.png", 1),  # 1 weight
    ("racer/bitcoin.png", 3), # 3 weight
    ("racer/vedro.png", 4)    # 4  weight
]
coin_weights = [80, 15, 5]  # Probability weights

done = False

# Player default position
pl_x = 300
pl_y = 500

# Enemy default position
enemy_pos_y = -1
enemy_pos_x = random.randint(100, 500)
speed = 5

# Create first coin
coin_img, coin_value = random.choices(coin_types, weights=coin_weights, k=1)[0]
coin_pos_x = random.randint(100, 500)
coin_pos_y = -1
coins = Coin(coin_pos_x, coin_pos_y, speed, coin_img, coin_value)

while not done:
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

    pygame.display.set_caption(f"Level: {Level}   RACER   Score: {Score}   Coins: {coin_score}")

    # Player movement
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        pl_x -= 10
    elif key[pygame.K_RIGHT]:
        pl_x += 10

    # Creating objects 
    player = Player(pl_x, pl_y)
    enemy = Enemy(enemy_pos_x, enemy_pos_y, speed)

    enem = enemy.image()
    car = player.image()
    coin_rect = coins.image()

    # speed adjustiong of objects
    enemy_pos_y += speed
    coins.y += speed - 2

    # Collision with enemy
    if car.colliderect(enem) or car.left > 500 or car.right < 100:
        pygame.mixer.music.load(musics[1])
        pygame.mixer.music.play()
        screen.fill(White)
        screen.blit(message, message_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
        done = True
        break

    # Collision with coin
    if car.colliderect(coin_rect):
        coin_sound = pygame.mixer.Sound("racer/coins-135571.mp3")
        coin_sound.play()
        coin_score += coins.value

        # Create new coin
        coin_img, coin_value = random.choices(coin_types, weights=coin_weights, k=1)[0]
        coin_pos_x = random.randint(100, 500)
        coin_pos_y = -1
        coins = Coin(coin_pos_x, coin_pos_y, speed, coin_img, coin_value)

    # Drawing everything
    screen.blit(bg, bg_rect)
    screen.blit(player.im, car)
    screen.blit(enemy.im, enem)
    screen.blit(coins.im, coin_rect)

    # Create new enemy if it go over the screen
    if enem.top > 600:
        enemy_pos_x = random.randint(100, 500)
        enemy_pos_y = -1
        Score += 1

    # Create new coin if it go over the screen
    if coins.y > 600:
        coin_img, coin_value = random.choices(coin_types, weights=coin_weights, k=1)[0]
        coin_pos_x = random.randint(100, 500)
        coin_pos_y = -10
        coins = Coin(coin_pos_x, coin_pos_y, speed, coin_img, coin_value)

    # New level condition
    if Score > 5:
        Level += 1
        Score = 0
        speed += 5

    pygame.display.flip()
    clock.tick(60)
