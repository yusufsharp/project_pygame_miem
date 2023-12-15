import pygame as pg
from pygame import *
import sys
from settings import *


class Platform(sprite.Sprite):
    def __init__(self, x, y, image_path):
        sprite.Sprite.__init__(self)
        self.image = image.load(image_path)
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class MovingPlatform(Platform):
    def __init__(self, x, y, image_path, start_x, end_x, speed):
        super().__init__(x, y, image_path)
        self.image = pg.transform.scale(self.image, (200, 32))
        self.rect = Rect(x, y, 200, 32)
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1  # 1 - right, -1 - left
        self.hero = None

    def set_hero(self, hero):
        self.hero = hero

    def update(self, count_moving_platforms):
        self.rect.x += self.direction * self.speed

        if self.rect.right > self.end_x or self.rect.left < self.start_x:
            self.direction *= -1
        if self.hero.on_moving_platform:
            self.hero.rect.x += self.direction * (self.speed // count_moving_platforms)



class Lava(Platform):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])
        self.images = [image.load(image_path) for image_path in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.animation_speed = 0.2
        self.animation_timer = pg.time.get_ticks()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.animation_timer > self.animation_speed * 1000:
            self.animation_timer = now
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

class Teleport(Platform):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
