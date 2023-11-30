import pygame as pg
from pygame import *
import sys
from settings import *


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, image_path):
        sprite.Sprite.__init__(self)
        self.image = image.load(image_path)
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
