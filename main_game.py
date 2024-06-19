import pygame
import os

pygame.init()

WIDTH = 1200
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Background.png")), (WIDTH, HEIGHT))
FPS = 60

JUMP_HEIGHT = 50
JUMP_SLOW = 30
GRAVITY = 5
HITBOX_WIDTH, HITBOX_HEIGHT = 20, 70
velocity = 0
ACCELERATION = 0.5
MAX_VELOCITY = 5
FRICTION = 0.1
X = WIDTH // 2
Y = HEIGHT - HITBOX_HEIGHT
HITBOX = pygame.Rect(X, Y, HITBOX_WIDTH, HITBOX_HEIGHT)

def draw():
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, (255, 0, 0), HITBOX)
    pygame.display.update()

def player_movements():
    global velocity, X
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        velocity += ACCELERATION
    elif keys[pygame.K_a]:
        velocity -= ACCELERATION
    else:
        if velocity > 0:
            velocity -= FRICTION
            if velocity < 0:
                velocity = 0
        elif velocity < 0:
            velocity += FRICTION
            if velocity > 0:
                velocity = 0

    if velocity > MAX_VELOCITY:
        velocity = MAX_VELOCITY
    elif velocity < -MAX_VELOCITY:
        velocity = -MAX_VELOCITY

    X += velocity
    if X < 0:
        X = 0
        velocity = 0
    elif X + HITBOX_WIDTH > WIDTH:
        X = WIDTH - HITBOX_WIDTH
        velocity = 0

    HITBOX.x = X

def player_jump():
    global decent, Jump
    if decent == False:
        if HEIGHT - (JUMP_HEIGHT + HITBOX_HEIGHT + JUMP_SLOW) < HITBOX.y:
            HITBOX.y -= 3
            if HEIGHT - (JUMP_HEIGHT + HITBOX_HEIGHT) < HITBOX.y:
                HITBOX.y -= 2
        else:
            decent = True
    if decent == True:
        if HITBOX.y < HEIGHT - HITBOX_HEIGHT:
            HITBOX.y += 3
        else:
            Jump = False
            decent = False



def gravity():
    if HITBOX.y < HEIGHT - HITBOX_HEIGHT:
        HITBOX.y += GRAVITY

def main():
    global run, Jump, decent
    Jump = False
    decent = False
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    Jump = True
            if event.type == pygame.QUIT:
                run = False
        if Jump == False:
            gravity()
        elif Jump == True:
            player_jump()
        player_movements()
        draw()
    pygame.quit()
main()
