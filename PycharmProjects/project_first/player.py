import pygame
import sys
from settings import *
from pygame.locals import *
from blocks import Platform


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets_sprites/idle_hero/Swordsman0000.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect()

        self.stand_image = pygame.image.load("assets_sprites/idle_hero/Swordsman0000.png")
        self.stand_image = pygame.transform.scale(self.stand_image, (128, 128))

        # Position and direction
        self.vx = 0  # компонента скорости по оси х
        self.pos = vec((340, 240))  # вектор, представляющий позицию персонажа на экране
        self.vel = vec(0, 0)  # вектор скорости персонажа
        self.acc = vec(0, 0)  # вектор ускорения
        self.direction = "RIGHT"

        self.jumping = False
        self.running = False
        self.move_frame = 0  # отслеживание текущего кадра персонажа

        # Анимация бега вправо

        self.run_ani_r = [pygame.image.load("assets_sprites/walking_hero/hero-running01_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running02_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running03_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running04_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running05_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running06_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running07_R.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running08_R.png")]

        # анимка влево
        self.run_ani_l = [pygame.image.load("assets_sprites/walking_hero/hero-running01_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running02_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running03_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running04_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running05_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running06_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running07_L.png"),
                          pygame.image.load("assets_sprites/walking_hero/hero-running08_L.png")]

    def move(self, entities):
        self.acc = vec(0, 0.5)  # ускорение персонажа вниз - имитация гравитации

        if abs(self.vel.x) > 0.3:  # определяем бежит ли персонаж, используется для анимации
            self.running = True
        else:
            self.running = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_a]:
            self.acc.x = -ACC  # бежим влево - отрицательное ускорение
        if pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # if self.pos.x > WINDOW_WIDTH:
        #     self.pos.x = 0
        # if self.pos.x < 0:
        #     self.pos.x = WINDOW_WIDTH

        self.rect.midbottom = self.pos  # обновляем прямоугольник, который используется для отрисовки персонажа

    def gravity_check(self, entities):
        hits = pygame.sprite.spritecollide(self, entities, False)
        for hit in hits:
            if self.vel.y > 0 and self.pos.y < hit.rect.bottom:
                self.pos.y = hit.rect.top + 1
                self.vel.y = 0
                self.jumping = False

    # def collide_check(self, entities):
    #     hits = pygame.sprite.spritecollide(self, entities, False)
    #     if self.vel.x > 0 or self.vel.x < 0:
    #         if hits:




    def update(self):
        if self.move_frame > 7:
            self.move_frame = 0
            return
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = self.run_ani_r[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = self.run_ani_l[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1

        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.run_ani_r[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.run_ani_l[self.move_frame]
        # elif not self.running:
        #     self.image = self.stand_image

    def attack(self):
        pass

    def jump(self, entities):
        self.rect.x += 1

        hits = pygame.sprite.spritecollide(self, entities, False)

        self.rect.x -= 1

        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
