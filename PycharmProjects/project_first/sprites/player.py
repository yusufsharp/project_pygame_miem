import pygame
from sprites.sprites import GameObject
from pygame.locals import *


class Player(GameObject):
    def __init__(self, start_x, start_y):
        super().__init__("sprites/assets_sprites/idle_hero/Swordsman0000.png", start_x, start_y)

        self.stand_image = self.image

        self.image_index = 0

        # Список изображений для анимации
        self.animation_images = [
            pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0000.png"),
            pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0001.png"),
            pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0002.png"),
            pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0003.png"),
        ]

        # Индекс текущего изображения
        self.image_index = 0

        # Таймер для управления скоростью анимации
        self.animation_timer = pygame.time.get_ticks()


    def update(self):

        if pygame.time.get_ticks() - self.animation_timer > 150:
            self.animation_timer = pygame.time.get_ticks()
            self.image_index = (self.image_index + 1) % len(self.animation_images)
            self.image = self.animation_images[self.image_index]

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= 5
        if keys[K_RIGHT]:
            self.rect.x += 5
        if keys[K_UP]:
            self.rect.y -= 5
        if keys[K_DOWN]:
            self.rect.y += 5