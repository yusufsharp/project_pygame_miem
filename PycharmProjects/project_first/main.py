import pygame
import sys
from utils.settings import *
from pygame.locals import *

pygame.init()

BACKGROUND = (0, 0, 0)
vec = pygame.math.Vector2  # creating vector object

# pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("media/images/Ground.png")
        self.image = pygame.transform.scale(self.image, (1920, 150))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - self.image.get_height() // 4))

        self.rect.width = WINDOW_WIDTH

    def render(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("objects/assets_sprites/idle_hero/Swordsman0000.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0  # компонента скорости по оси х
        self.pos = vec((340, 240))  # вектор, представляющий позицию персонажа на экране
        self.vel = vec(0, 0)  # вектор скорости персонажа
        self.acc = vec(0, 0)  # вектор ускорения
        self.direction = "RIGHT"

        self.jumping = False

    def move(self):
        self.acc = vec(0, 0.5)  # ускорение персонажа вниз - имитация гравитации

        if abs(self.vel.x) > 0.3:  # определяем бежит ли персонаж, используется для анимации
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC  # бежим влево - отрицательное ускорение
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WINDOW_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WINDOW_WIDTH

        self.rect.midbottom = self.pos  # обновляем прямоугольник, который используется для отрисовки персонажа

    def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def update(self):
        pass

    def attack(self):
        pass

    def jump(self):
        pass


# classes
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
player = Player()

while True:
    player.gravity_check()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BACKGROUND)

    # render func
    player.move()
    ground.render()
    screen.blit(player.image, player.rect)

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
