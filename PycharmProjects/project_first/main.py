import pygame as pg
import sys
from utils.settings import *
from sprites.player import Player

pg.init()

bg = (255, 255, 255)
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
all_sprites = pg.sprite.Group(player)



def main():
    while True:
        screen.fill(bg)
        all_sprites.draw(screen)
        clock = pg.time.Clock()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        all_sprites.update()

        pg.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    main()
