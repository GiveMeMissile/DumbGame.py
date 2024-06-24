import pygame
import os

pygame.init()

# Window control
WIDTH = 1200
HEIGHT = 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Background.png")), (WIDTH, HEIGHT))
FPS = 60

# Player settings
JUMP_HEIGHT = 70
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
JUMP_SOUND = pygame.mixer.Sound("Stuff/Jump_sound.mp3")

#Platfrom settings
PLATFORM_HEIGHT = 60
PLATFORM_WIDTH = 200
PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Platform.png.png")), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

platforms = []
initial_height = HEIGHT
def draw():
    platform_location_x = 100
    platform_location_y = 550
    WINDOW.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WINDOW, (255, 0, 0), HITBOX)
    for _ in range(10):
        WINDOW.blit(PLATFORM, (platform_location_x, platform_location_y))
        platforms.append([platform_location_x, platform_location_y])
        platform_location_x += PLATFORM_WIDTH + 50
        platform_location_y -= PLATFORM_HEIGHT
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
    global decent, Jump, initial_height
    if decent == False:
        if initial_height - (JUMP_HEIGHT + HITBOX_HEIGHT + JUMP_SLOW) < HITBOX.y:
            HITBOX.y -= 3
            if HEIGHT - (JUMP_HEIGHT + HITBOX_HEIGHT) < HITBOX.y:
                HITBOX.y -= 4
        else:
            decent = True
    if decent == True:
        HITBOX.y += GRAVITY
        for platform_location_x, platform_location_y in platforms:
            platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
                HITBOX.y = platform_rect.y - HITBOX_HEIGHT
                Jump = False
                decent = False
                initial_height = HITBOX.y
        if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
            HITBOX.y = HEIGHT - HITBOX_HEIGHT
            Jump = False
            decent = False
            initial_height = HEIGHT - HITBOX_HEIGHT



def gravity():
    HITBOX.y += GRAVITY
    for platform_location_x, platform_location_y in platforms:
        platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
            HITBOX.y = platform_rect.y - HITBOX_HEIGHT
            return
    if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
        HITBOX.y = HEIGHT - HITBOX_HEIGHT


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
                if event.key == pygame.K_w and Jump == False:
                    Jump = True
                    JUMP_SOUND.play()
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
