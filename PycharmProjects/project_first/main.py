import pygame as pg, pygame
from pygame import *
import sys
import blocks
from blocks import Platform
from settings import *
from pygame.locals import *
import player
from player import Player
from menu import menuFunc
pg.init()


background_image = pg.image.load(BACKGROUND_IMAGE)
background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_WIDTH))
overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))  # Черный цвет для затемнения
overlay.set_alpha(230)  # Настройка уровня прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

entities = pygame.sprite.Group()
platforms = []
hero = Player(55,55) # создаем героя по (x,y) координатам
entities.add(hero)

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

def main():
    run = True
    reg = False
    left = right = up = False  # по умолчанию — стоим
    while run:
        clock = pg.time.Clock()
        bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        if not reg:
            reg = menuFunc()
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True

                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False

                if e.type == KEYDOWN and e.key == K_UP:
                    up = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False

            bg.fill(Color(BACKGROUND_COLOR))
            screen.blit(background_image, (0, 0))
            screen.blit(overlay, (0, 0))

            entities.draw(screen)
            hero.update(left, right, up, platforms)
            entities.draw(screen)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == '__main__':
    main()