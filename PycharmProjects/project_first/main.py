import pygame as pg
from pygame import *
import sys
from utils.settings import *
import blocks
from blocks import Platform


entities = pg.sprite.Group()
platforms = []

x = y = 0
for row in level:
    for col in row:
        if col != ' ':
            pf = Platform(x, y, IMGS_PLATFORM[col])
            entities.add(pf)
            platforms.append(pf)
        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

background_image = pg.image.load(BACKGROUND_IMAGE)
background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_WIDTH))
overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))  # Черный цвет для затемнения
overlay.set_alpha(230)  # Настройка уровня прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    bg.fill(Color(BACKGROUND_COLOR))
    run = True
    while run:
        clock = pg.time.Clock()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

        screen.blit(background_image, (0, 0))
        screen.blit(overlay, (0, 0))
        entities.draw(screen)
        pg.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()