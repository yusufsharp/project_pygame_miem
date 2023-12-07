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
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1 #1 - right, -1 - left

    def update(self):
        self.rect.x += self.direction * self.speed

        if self.rect.right > self.end_x or self.rect.left < self.start_x:
            self.direction *= -1