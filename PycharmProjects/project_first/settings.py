
import pygame.time
import pyganim
import pygame
from pygame.locals import *
from enemies import *

SECURE_KEY = "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?"
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080


FPS = 60
FPS_CLOCK = pygame.time.Clock()

BACKGROUND_IMAGE = 'images/Background.jpg'
BACKGROUND_COLOR = '#320236'
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = '#FF6262'
IMGS_PLATFORM = {
    '-': 'images/blocks/IndustrialTile_32.png',  # потолок
    '_': 'images/blocks/IndustrialTile_50.png',  # пол
    '/': 'images/blocks/IndustrialTile_40.png',  # верхняя линия слева
    "\\": 'images/blocks/IndustrialTile_42.png',  # верхняя линия справа
    '1': 'images/blocks/IndustrialTile_31.png',  # левый верхний угол
    '2': "images/blocks/IndustrialTile_33.png",  # правый верхний угол
    '3': 'images/blocks/IndustrialTile_49.png',  # левый нижний угол
    '4': 'images/blocks/IndustrialTile_51.png',  # левый нижний угол
    '*': "images/blocks/IndustrialTile_68.png",  # сводка
    '&': 'images/blocks/IndustrialTile_52.png',  # платформа от стены
    '^': 'images/blocks/transform_platform.png', #двигающаяся платформа
    'T': 'images/teleport.png'            #телепорт
}

lava_images = ['images/lava/lava1.png',
               'images/lava/lava2.png',
               'images/lava/lava3.png',
               'images/lava/lava4.png']


level1 = [
    '---------------------------------------------------------------------------------------------------------------------------------------------------------',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                   &&                                                                                 \\',
    '/                                   T                                                                                                                  \\',
    '/                                   &                                                                                                                  \\',
    '/                                                                                                                                                      \\',
    '/                                                  &                                      &&                                                           \\',
    '/                                                                           &&                                                                         \\',
    '/                                                                                                        &&                                            \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                               p                                                                      \\',
    '/                                                                                                                &                                     \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                   p                                                                                                  \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                    &&                                                           &&&          &&                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                     m                                                                                                \\',
    '/                                                  &&&&&&&                                                                                             \\',
    '/                                                                                                                                                      \\',
    '/                              &&                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                  m                                                                   \\',
    '/                                 &              &        &&         &&&&&      &&&&&&&    &&&&    &&   &&&                                            \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                 &&&                                   \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                             &&                                       \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                      g             g                g            g                                                   \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                               &&&&&&&&&&&      &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&        &&&                                \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL    \\',
    '/                                                                                                                                                      \\',
    '________________________________________________________________________________________________________________________________________________________',
]

level2 = [
    '---------------------------------------------------------------------------------------------------------------------------------------------------------',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                   &&                                                                                 \\',
    '/                                                                                                                                                      \\',
    '/                                   &                                                                                                                  \\',
    '/                                                                                                                                                      \\',
    '/                                                  &                                      &&                                                           \\',
    '/                                                                           &&                                                                         \\',
    '/                                                                                                        &&                                            \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                &                                     \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                    &&                                                           &&&          &&                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                  &&&&&&&                                                                                             \\',
    '/                                                                                                                                                      \\',
    '/                              &&                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                 &              &        &&         &&&&&      &&&&&&&    &&&&    &&   &&&                                            \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                 &&&                                   \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                             &&                                       \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                               &&&&&&&&&&&      &&&&&&&&   &&&&&&&&       &&&&&&&&&&&&&         &&&&&&&&&&&        &&&                                \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/                                                                                                                                                      \\',
    '/LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL    \\',
    '/                                                                                                                                                      \\',
    '________________________________________________________________________________________________________________________________________________________',
]
levels = [level1, level2]