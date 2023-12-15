import pygame
from enemies import *
from blocks import *
from settings import *
from pygame.locals import *
from player import Player
from menu import menu_func, death_screen, stat_request, send_patch_request
from player import AttackEffect
from player import Player, Coin, StatusBar

pg.init()

background_image = pg.image.load(BACKGROUND_IMAGE)
background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_WIDTH))
overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))  # Черный цвет для затемнения
overlay.set_alpha(230)  # Настройка уровня прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

#marat

def load_level(level):
    global entities, platforms, hero, monsters, moving_platform, status, attack_effect
    entities = pygame.sprite.Group()
    platforms = []  # создаем героя по (x,y) координатам

    hero = Player(1064, 2000, username = 'Дрочеслав')  # создаем героя по (x,y) координатам
    status = StatusBar(800, 900, screen)
    attack_effect = AttackEffect(hero)

    monsters = pygame.sprite.Group()

    moving_platform = MovingPlatform(2064, 900, IMGS_PLATFORM['^'], 2064, 2904, 3)
    moving_platform.set_hero(hero)
    entities.add(hero, moving_platform)
    entities.add(attack_effect)
    platforms.append(moving_platform)

    x = y = 0
    for row in level:
        for col in row:
            if col != ' ' and col != 'L' and col != 'T' and col != 'm' and col != 'g':
                pf = Platform(x, y, IMGS_PLATFORM[col])
                entities.add(pf)
                platforms.append(pf)
            elif col == 'L':
                lava = Lava(x, y, lava_images)
                entities.add(lava)
                platforms.append(lava)
            elif col == 'T':
                tp = Teleport(x, y, IMGS_PLATFORM[col])
                entities.add(tp)
                platforms.append(tp)
            elif col == 'm':
                mn = Enemy(x, y, 2, 0, 100, 0, 30)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            elif col == 'g':
                gm = Enemy2(x, y, 1, 0, 200, 0, hero, 150)
                entities.add(gm)
                platforms.append(gm)
                monsters.add(gm)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


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
    current_level = 0
    run = True
    username = 'АНОНИМУС'
    reg = False
    load_level(levels[current_level])
    attack = left = right = up = False  # по умолчанию — стоим
    total_level_width = len(levels[current_level][0]) * PLATFORM_WIDTH
    total_level_height = len(levels[current_level][0]) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    while run:


        clock = pg.time.Clock()
        bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        if not reg:
            reg, username = menu_func()
            print(f'ИМЯ ПОЛЬЗОВАТЕЛЯ: {username}')
            send_patch_request(username, "health", 1000)
            print(stat_request(username))
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

        if hero.next_level and current_level == 0:
            current_level += 1
            load_level(levels[current_level])
            hero.next_level = False

        camera.update(hero)
        for e in entities:
            if isinstance(e, Lava):
                e.animate()
            if not isinstance(e, Player):  # Отрисовываем телепорт перед героем
                screen.blit(e.image, camera.apply(e))

        screen.blit(hero.image, camera.apply(hero))
        hero.update(left, right, up, platforms, attack, screen)
        moving_platform.update()
        monsters.update(platforms)
        hero.draw_health_bar(screen)
        status.update(hero, clock)
        attack_effect.update(attack, platforms, hero)


        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
