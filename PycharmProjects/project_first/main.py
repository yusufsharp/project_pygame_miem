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
player_instance = Player()

entities = pygame.sprite.Group()
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

def main():
    run = True
    reg = False  # menu by Yusuf
    while run:
        if not reg:
            reg = menuFunc()      # menu running
            # жми кнопку войти чтобы начать играть
        else:
            player_instance.gravity_check(entities)
            clock = pg.time.Clock()
            bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_instance.jump(entities)

            bg.fill(Color(BACKGROUND_COLOR))
            screen.blit(background_image, (0, 0))
            screen.blit(overlay, (0, 0))

            entities.draw(screen)


            player_instance.update()
            player_instance.move(entities)
            screen.blit(player_instance.image, player_instance.rect)

        pygame.display.update()

if __name__ == '__main__':
    main()