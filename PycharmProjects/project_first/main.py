import pygame
from enemies import *
from blocks import *
from settings import *
from pygame.locals import *
from player import Player, AttackEffect
from player import Player, Coin, StatusBar
from menu import menuFunc, death_screen

pg.init()

background_image = pg.image.load(BACKGROUND_IMAGE)
background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_WIDTH))
overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))  # Черный цвет для затемнения
overlay.set_alpha(230)  # Настройка уровня прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

entities = pygame.sprite.Group()
platforms = []  # создаем героя по (x,y) координатам

hero = Player(1064, 2000, username= "Дрочеслав")  # создаем героя по (x,y) координатам
status = StatusBar(800, 900, screen)
attack_effect = AttackEffect(hero)
entities.add(attack_effect)

moving_platform = MovingPlatform(2064, 900, IMGS_PLATFORM['^'], 2064, 2904, 3)
moving_platform.set_hero(hero)
entities.add(hero, moving_platform)
platforms.append(moving_platform)

x = y = 0

for row in level:
    for col in row:
        if col != ' ' and col != 'L':
            pf = Platform(x, y, IMGS_PLATFORM[col])
            entities.add(pf)
            platforms.append(pf)
        elif col == 'L':
            lava = Lava(x, y, lava_images)
            entities.add(lava)
            platforms.append(lava)
        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

monsters = pygame.sprite.Group()
mn = Enemy(2600, 1095, 2, 0, 100, 0, 30)
mn2 = Enemy(2300, 1095, 2, 0, 100, 0, 30)
golem1 = Enemy2(2000, 1888, 1, 0, 200, 0, hero, 150)
entities.add(mn)
entities.add(mn2)
entities.add(golem1)
platforms.append(mn)
platforms.append(mn2)
platforms.append(golem1)
monsters.add(mn, mn2, golem1)

coin = Coin(2333, 1888)
entities.add(coin)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2

    return Rect(l, t, w, h)


def main():
    run = True
    reg = True
    username = 'АНОНИМУС'
    attack = left = right = up = False  # по умолчанию — стоим
    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level[0]) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    while run:

        attack_effect.update(attack, platforms, hero)

        clock = pg.time.Clock()
        bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        if not reg:
            reg, username = menuFunc()
            print(f'ИМЯ ПОЛЬЗОВАТЕЛЯ: {username}')
        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == KEYDOWN and e.key == K_a:
                    left = True
                if e.type == KEYDOWN and e.key == K_d:
                    right = True

                if e.type == KEYUP and e.key == K_d:
                    right = False
                if e.type == KEYUP and e.key == K_a:
                    left = False

                if e.type == KEYDOWN and e.key == K_w:
                    up = True

                if e.type == KEYUP and e.key == K_w:
                    up = False

                if e.type == KEYDOWN and e.key == K_SPACE:
                    attack = True
                if e.type == KEYUP and e.key == K_SPACE:
                    attack = False

        bg.fill(Color(BACKGROUND_COLOR))
        screen.blit(background_image, (0, 0))
        screen.blit(overlay, (0, 0))

        hero.update(left, right, up, platforms, attack)

        camera.update(hero)
        for e in entities:
            if isinstance(e, Lava):
                e.animate()


            screen.blit(e.image, camera.apply(e))
        moving_platform.update()

        coin.update(hero)

        monsters.update(platforms)

        hero.draw_health_bar(screen)
        status.update(hero, clock)


        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
