import pygame
import random

pygame.init()

from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    K_SPACE,
    KEYDOWN,
    QUIT
)

screen = pygame.display.set_mode((900, 800))

#Creating a custom event for adding an enemy 
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)

#Setup for sounds
pygame.mixer.init()
pygame.mixer.music.load("./sounds/back_music.mp3")
pygame.mixer.music.play(loops=-1)

collission_sound = pygame.mixer.Sound("./sounds/collission.ogg")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./images/jet.png').convert()
        self.surf = pygame.transform.scale(self.surf, (170, 100))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -15)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 15)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 900:
            self.rect.right = 900
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom > 800:
            self.rect.bottom = 800

    def current_position(self):
        return (self.rect.x+self.rect.width, self.rect.y+int(self.rect.height/2))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./images/missile.png').convert()
        self.surf = pygame.transform.scale(self.surf, (100, 50))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(900, 1000),
                random.randint(0, 800)
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        elif pygame.sprite.spritecollideany(self, fires):
            collission_sound.play()
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./images/cloud.png').convert()
        self.surf = pygame.transform.scale(self.surf, (150, 90))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(920, 1020),
                random.randint(0, 800)
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


class Fire(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('./images/fire.png').convert()
        self.surf = pygame.transform.scale(self.surf, (100, 70))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=player.current_position()
        )

    def update(self):
        self.rect.move_ip(65, 0)
        if self.rect.right > 900:
            self.kill()

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
fires = pygame.sprite.Group()
all_sprites.add(player)

#Setting up clock for framerate
clock = pygame.time.Clock()

running=True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running=False
            elif event.key == K_SPACE:
                new_fire = Fire()
                fires.add(new_fire)
                all_sprites.add(new_fire)
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    #Filling the screen with sky blue
    screen.fill((135, 206, 250))
    
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Calling update method on the enemies sprite group which will update every enemy within Sprite Group
    enemies.update()
    clouds.update()
    fires.update()

    # Collission detection
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # if pygame.sprite.spritecollideany(new_fire, enemies):
    #     enemies.kill()

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

