import pygame as pg
import sys
from utils.settings import *

pg.init()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def main():
    run = True
    while run:
        clock = pg.time.Clock()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

        pg.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()