import pygame.time
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
#1920 1080

# physics
ACC = 1
FRIC = -0.2125
COUNT = 0
FPS = 60
FPS_CLOCK = pygame.time.Clock()


BACKGROUND_IMAGE = 'images/Background.jpg'
BACKGROUND_COLOR = '#320236'
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = '#FF6262'
IMGS_PLATFORM = {
       '-': 'images/blocks/IndustrialTile_32.png', #потолок
       '_': 'images/blocks/IndustrialTile_50.png', #пол
       '/': 'images/blocks/IndustrialTile_40.png', #верхняя линия слева
       "\\": 'images/blocks/IndustrialTile_42.png', #верхняя линия справа
       '1': 'images/blocks/IndustrialTile_31.png',#левый верхний угол
       '2': "images/blocks/IndustrialTile_33.png", # правый верхний угол
       '3': 'images/blocks/IndustrialTile_49.png', # левый нижний угол
       '4': 'images/blocks/IndustrialTile_51.png', # левый нижний угол
       '*': "images/blocks/IndustrialTile_68.png", #сводка
       '&': 'images/blocks/IndustrialTile_52.png', #платформа от стены
}

level = [
       "1----------------------------------------------------------2",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                     ---  \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/    &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&*",
       "/                                                          \\",
       "/                                                          \\",
       "*&&                                                        \\",
       "/                                                          \\",
       "/                                                          \\",
       "/     --                                                   \\",
       "/                                                          \\",
       "*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&       \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                     &&&&&*",
       "/                                                          \\",
       "/                                                          \\",
       "/                                                          \\",
       "3__________________________________________________________4"]
vec = pygame.math.Vector2  # creating vector object
