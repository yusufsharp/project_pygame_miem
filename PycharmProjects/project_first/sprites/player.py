import pygame
from sprites.sprites import GameObject
from pygame.locals import *


class Player(GameObject):
    def __init__(self, start_x, start_y):
        super().__init__("sprites/assets_sprites/idle_hero/Swordsman0000.png", start_x, start_y)

        # Список изображений для анимации
        self.animation_images = [
            pygame.transform.scale(pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0000.png"), (128, 128)),
            pygame.transform.scale(pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0001.png"), (128, 128)),
            pygame.transform.scale(pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0002.png"), (128, 128)),
            pygame.transform.scale(pygame.image.load("sprites/assets_sprites/idle_hero/Swordsman0003.png"), (128, 128)),
        ]
        # ходьба
        self.walk_cycle = [pygame.image.load(f"sprites/assets_sprites/walking_hero/hero-running-separated{i}.png") for i
                           in range(2, 10)]
        self.facing_left = False
        # Индекс текущего изображения
        self.image_index = 0
        self.speed = 5

        # Таймер для управления скоростью анимации
        self.animation_timer = pygame.time.get_ticks()

    def update(self):

        if pygame.time.get_ticks() - self.animation_timer > 150:
            self.animation_timer = pygame.time.get_ticks()
            self.image_index = (self.image_index + 1) % len(self.animation_images)
            self.image = self.animation_images[self.image_index]

        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            self.rect.x -= 15
        if keys[K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            self.rect.x += 15
        if keys[K_UP]:
            self.rect.y -= 1
        if keys[K_DOWN]:
            self.rect.y += 1

    def walk_animation(self):
        self.image = self.walk_cycle[self.image_index]
        if self.facing_left:
            self.image = pygame.transform.scale(self.image, (128, 128))
            self.image = pygame.transform.flip(self.image, True, False)  # Поворачиваем изображение по горизонтали
        else:
            self.image = pygame.transform.scale(self.image, (128, 128))
        if self.image_index < len(self.walk_cycle) - 1:
            self.image_index += 1
        else:
            self.image_index = 0
