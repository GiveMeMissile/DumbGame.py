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
GRAVITY = 7
HITBOX_WIDTH, HITBOX_HEIGHT = 20, 70
MAX_ATTACK = 100
velocity = 0
ACCELERATION = 0.5
MAX_VELOCITY = 5
FRICTION = 0.1
X = WIDTH // 2
Y = HEIGHT - HITBOX_HEIGHT

JUMP_SOUND = pygame.mixer.Sound("Stuff/Jump_sound.mp3")
ATTACK_SOUND = pygame.mixer.Sound("Stuff/Sword_Draw.mp3")

HITBOX = pygame.Rect(X, Y, HITBOX_WIDTH, HITBOX_HEIGHT)
PLAYER_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Stickboy.png.png")), (HITBOX_WIDTH + 30, HITBOX_HEIGHT + 20))
ATTACK_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Attack_posistion.png")), (HITBOX_WIDTH + 90, HITBOX_HEIGHT + 20))

# Platform settings
PLATFORM_HEIGHT = 60
PLATFORM_WIDTH = 200
PLATFORM = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Platform.png.png")), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

#Enemy settings
ENEMY_RED_HITBOX_WIDTH, ENEMY_RED_HITBOX_HEIGHT = 40, 70

ENEMY_RED_HITBOX = pygame.Rect(100, HEIGHT - ENEMY_RED_HITBOX_HEIGHT, ENEMY_RED_HITBOX_WIDTH, ENEMY_RED_HITBOX_HEIGHT)
AMONG_RED_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Stuff", "Among_red.png.png")), (ENEMY_RED_HITBOX_WIDTH, ENEMY_RED_HITBOX_HEIGHT))
enemy_red_hitbox = pygame.Rect(100, HEIGHT - ENEMY_RED_HITBOX_HEIGHT, ENEMY_RED_HITBOX_WIDTH,
                                   ENEMY_RED_HITBOX_HEIGHT)
platforms = []

def draw():
    platform_location_x = 100
    platform_location_y = 550
    WINDOW.blit(BACKGROUND, (0, 0))
    if attack == False:
        WINDOW.blit(PLAYER_IMAGE, (HITBOX.x - 15, HITBOX.y - 10))
    else:
        WINDOW.blit(ATTACK_IMAGE, (HITBOX.x - 45, HITBOX.y - 10))
    WINDOW.blit(AMONG_RED_IMAGE, (ENEMY_RED_HITBOX.x, ENEMY_RED_HITBOX.y))
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

def player_attack():
    global attack, attack_limit, attack_area
    if attack == True:
        attack_limit += 5
        attack_area = pygame.Rect((HITBOX.x - 35, HITBOX.y), (90, 20))
        attack_aura.append(attack_area)
    if attack_limit >= MAX_ATTACK:
        for attack_area in attack_aura:
            attack_aura.remove(attack_area)
        attack = False


def player_jump():
    global decent, Jump, initial_height, falling
    if decent == False:
        if HITBOX.y > initial_height - (JUMP_HEIGHT + HITBOX_HEIGHT + JUMP_SLOW):
            HITBOX.y -= 3
            if initial_height - (JUMP_HEIGHT + HITBOX_HEIGHT) < HITBOX.y:
                HITBOX.y -= 4
        else:
            decent = True
    if decent:
        HITBOX.y += GRAVITY
        for platform_location_x, platform_location_y in platforms:
            platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
                HITBOX.y = platform_rect.y - HITBOX_HEIGHT
                decent = False
                Jump = False
                initial_height = HITBOX.y
                return
        if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
            HITBOX.y = HEIGHT - HITBOX_HEIGHT
            decent = False
            Jump = False
            initial_height = HEIGHT - HITBOX_HEIGHT

def gravity():
    global initial_height, falling
    if Jump == False:
        falling = True
        for platform_location_x, platform_location_y in platforms:
            platform_rect = pygame.Rect(platform_location_x, platform_location_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            if HITBOX.colliderect(platform_rect) and HITBOX.bottom <= platform_rect.top + GRAVITY:
                HITBOX.y = platform_rect.y - HITBOX_HEIGHT
                initial_height = HITBOX.y
                falling = False
                return
        if HITBOX.y + HITBOX_HEIGHT >= HEIGHT:
            HITBOX.y = HEIGHT - HITBOX_HEIGHT
            initial_height = HEIGHT - HITBOX_HEIGHT
            falling = False
            return
        HITBOX.y += GRAVITY
    falling = False

def enemy_handler():
    global enemy_red_hitbox
    among_red_enemy.append(enemy_red_hitbox)
    for enemy_red_hitbox in among_red_enemy:
        if enemy_red_hitbox.colliderect(attack_area):
            among_red_enemy.remove(enemy_red_hitbox)

def main():
    global run, Jump, decent, falling, platforms, initial_height, attack, attack_limit, attack_aura, among_red_enemy
    attack_aura = []
    among_red_enemy = []
    falling = True
    attack = False
    Jump = False
    decent = False
    platforms = []
    initial_height = HEIGHT - HITBOX_HEIGHT
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not Jump and not falling:
                    Jump = True
                    JUMP_SOUND.play()
                if attack == False:
                    if event.key == pygame.K_SPACE:
                        attack = True
                        attack_limit = 0
                        ATTACK_SOUND.play()
            if event.type == pygame.QUIT:
                run = False
        if attack:
            player_attack()
        if not Jump:
            gravity()
        else:
            player_jump()

        player_movements()
        draw()
    pygame.quit()

main()
