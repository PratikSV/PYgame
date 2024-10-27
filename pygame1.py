import pygame
import random
import math

# Initialization of pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((1000, 600))

# Background image
bg_image = pygame.image.load('bg.png')

# Title and icon
pygame.display.set_caption("Blast asteroids")
icon = pygame.image.load('egal.png')
pygame.display.set_icon(icon)

# Player settings
playingimg = pygame.image.load('spaceship.png')
playerx = 450
playery = 450
playerx_change = 0

# Enemy settings
enemyimg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []

num_enemy = 5
for i in range(num_enemy):
    enemyimg.append(pygame.image.load('rock.png'))
    enemyx.append(random.randint(0, 924))
    enemyy.append(random.randint(50, 200))
    enemyx_change.append(3)
    enemyy_change.append(40)

# Bullet settings
bulletimg = pygame.image.load('bullet.png')
bulletx = 0
bullety = 450
bullety_change = 4
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 100)

def game_over(x, y):
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (x, y))

def show_score(x, y):
    score = font.render('Score:' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playingimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 20, y + 20))

def is_collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(math.pow((enemyx - bulletx), 2) + math.pow((enemyy - bullety), 2))
    return distance < 27

# Game loop
running = True
while running:
    screen.blit(bg_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerx += playerx_change

    # Keeping the player within bounds
    if playerx <= 0:
        playerx = 0
    if playerx >= 900:
        playerx = 900

    # Enemy movement and collision detection
    for i in range(num_enemy):
        # Game over
        if enemyy[i] > 410:
            for j in range(num_enemy):
                enemyy[j] = 2000  # Move enemies off-screen
            game_over(200, 250)
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 900:
            enemyx_change[i] = -3
            enemyy[i] += enemyy_change[i]

        # Collision
        collision = is_collision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            bullety = 450
            bullet_state = 'ready'
            score_value += 1
            enemyx[i] = random.randint(0, 924)
            enemyy[i] = random.randint(50, 200)

        enemy(enemyx[i], enemyy[i], i)

    # Bullet movement
    if bullety <= 0:
        bullety = 450
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    show_score(textx, texty)
    pygame.display.update()
