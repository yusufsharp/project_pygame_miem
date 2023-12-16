"""
Основной модуль игры.

Содержит инициализацию, основной цикл и загрузку уровней.

Модули:
- menu: Модуль для работы с пользовательским меню.
- player: Модуль, содержащий классы Player, StatusBar, AttackEffect и HealthBar.
- blocks: Модуль с классами платформ и препятствий.
- threading: Модуль для работы с многозадачностью.

Глобальные переменные:
- pg: Инициализация Pygame.
- background_image: Задний фон игры.
- overlay: Полупрозрачное затемнение для подложки.
- screen: Экран Pygame.
- icon: Иконка приложения.

Функции:
- load_level(level, screen, username, current_level, exp_data=0): Загружает уровень, создает персонажа, статус-бар и эффект атаки.
- Camera: Класс для работы с камерой игры.
- camera_configure(camera, target_rect): Конфигурирует положение камеры относительно персонажа.
- main(): Основной цикл игры.

Переменные:
- current_level: Текущий уровень.
- run: Флаг, указывающий на выполнение основного цикла.
- username: Имя пользователя.
- reg: Флаг, указывающий на необходимость регистрации пользователя.
- attack, left, right, up: Флаги состояний клавиш управления.
- total_level_width, total_level_height: Общая ширина и высота уровня.
- camera: Экземпляр класса Camera для управления камерой.
- start_time: Время начала уровня.
- clock: Таймер для ограничения частоты кадров.

Запуск игры:
- Вызывает функцию main(), запускающую основной цикл игры.
"""
from menu import *
from player import AttackEffect
from player import Player, StatusBar
from blocks import *
import threading

pg.init()

background_image = pg.image.load(BACKGROUND_IMAGE)
background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_WIDTH))
overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
overlay.fill((0, 0, 0))  # Черный цвет для затемнения
overlay.set_alpha(230)  # Настройка уровня прозрачности (0 - полностью прозрачный, 255 - непрозрачный)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)


# marat

def load_level(level, screen, username, current_level, exp_data=0):
    """
    Загружает уровень и создает соответствующие объекты.

    :param level: Список строк, представляющих уровень.
    :type level: list
    :param screen: Экран Pygame.
    :type screen: pygame.Surface
    :param username: Имя пользователя.
    :type username: str
    :param current_level: Текущий уровень.
    :type current_level: int
    :param exp_data: Дополнительные данные опыта (по умолчанию 0).
    :type exp_data: int
    """
    global entities, platforms, hero, monsters, moving_platforms, status, attack_effect, reg
    entities = pygame.sprite.Group()
    platforms = []  # создаем героя по (x,y) координатам
    exp = 0
    if current_level != 0:
        exp = exp_data
    hero = Player(1064, 1800, screen, username, exp)  # создаем героя по (x,y) координатам
    status = StatusBar(1700, 85, screen)
    attack_effect = AttackEffect(hero)

    monsters = pygame.sprite.Group()
    entities.add(attack_effect)

    moving_platforms = []

    x = y = 0
    for row in level:
        for col in row:
            if col != ' ' and col != 'L' and col != 'T' and col != 'm' and col != 'g' and col != 'p' and col != 'n' and col != 'S' and col != 'E':
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
            elif col == 'm' or col == 'n':
                if col == 'm':
                    mn = Enemy(x, y, 2, 0, 100, 0, 30)
                else:

                    mn = Enemy(x, y, 2, 0, 140, 0, 30)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            elif col == 'g':
                gm = Enemy2(x, y, 1, 0, 120, 0, hero, 150)
                entities.add(gm)
                platforms.append(gm)
                monsters.add(gm)
            elif col == 'p':
                moving_platform = MovingPlatform(x, y, IMGS_PLATFORM['^'], x, x + 1500, 4)
                moving_platform.set_hero(hero)
                entities.add(hero, moving_platform)
                platforms.append(moving_platform)
                moving_platforms.append(moving_platform)
            elif col == 'S':
                torch = Thorns(x, y)
                entities.add(torch)
                platforms.append(torch)
            elif col == 'E':
                gate = Gate(x, y, IMGS_PLATFORM['E'])
                entities.add(gate)
                platforms.append(gate)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


class Camera(object):
    """
    Класс Camera представляет собой камеру для отслеживания и перемещения по игровому миру.

    Attributes:
    - camera_func: Функция для обновления положения камеры.
    :type camera_func: Callable

    - state: Прямоугольник, представляющий текущее состояние камеры (положение и размеры).
    :type state: pygame.Rect
    """

    def __init__(self, camera_func, width, height):
        """
            Инициализирует объект камеры.

            :param camera_func: Функция для обновления положения камеры.
            :type camera_func: function
            :param width: Ширина камеры.
            :type width: int
            :param height: Высота камеры.
            :type height: int
            """
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        """
        Применяет положение камеры к цели.

        :param target: Объект, к которому применяется камера.
        :type target: pygame.sprite.Sprite

        """
        return target.rect.move(self.state.topleft)

    def update(self, target):
        """
              Обновляет положение камеры относительно цели.

              :param target: Объект, к которому привязана камера.
              :type target: pygame.sprite.Sprite
              """
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    """
    Функция для конфигурации положения камеры относительно цели.

    :param camera: Прямоугольник, представляющий текущее состояние камеры (положение и размеры).
    :type camera: pygame.Rect
    :param target_rect: Прямоугольник, представляющий цель, к которой привязана камера.
    :type target_rect: pygame.Rect

    :return: Новый прямоугольник, представляющий положение камеры после конфигурации.
    :rtype: pygame.Rect
    """
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WINDOW_WIDTH / 2, -t + WINDOW_HEIGHT / 2

    return Rect(l, t, w, h)


def main():
    """
     Основная функция игры.

     Управляет основным циклом игры, обрабатывает события и обновляет экран.
     """
    current_level = 0
    run = True
    username = 't'
    reg = False
    attack = left = right = up = False  # по умолчанию — стоим
    total_level_width = len(levels[current_level][0]) * PLATFORM_WIDTH
    total_level_height = len(levels[current_level][0]) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)
    start_time = pygame.time.get_ticks()
    while run:
        clock = pg.time.Clock()
        bg = Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        if not reg:
            reg, username = menu_func()
            stat_dict = stat_request(username)
            current_level = stat_dict['experience']
            exp_data = stat_dict['points']
            load_level(levels[current_level], screen, username, current_level, exp_data=exp_data)
            print(f'ИМЯ ПОЛЬЗОВАТЕЛЯ: {username}')
            print(stat_request(username))
            start_time = pygame.time.get_ticks()
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

        if hero.restart:
            start_time = pygame.time.get_ticks()
            load_level(levels[current_level], screen, username, current_level, exp_data=hero.exp)
            hero.restart = False
            left = right = up = attack = False
        bg.fill(Color(BACKGROUND_COLOR))
        screen.blit(background_image, (0, 0))
        screen.blit(overlay, (0, 0))

        if hero.next_level and current_level < len(levels):
            animation_thread = threading.Thread(target=darken_screen(screen, duration=6000))
            animation_thread.start()
            send_patch_request(username, 'completion_time', (pygame.time.get_ticks() - start_time) // 1000)
            send_patch_request(username, 'experience', current_level + 1)
            send_patch_request(username, 'points', hero.exp)
            animation_thread.join()
            left = right = up = False
            print(stat_request(username))
            current_level += 1
            load_level(levels[current_level], screen, username, current_level, exp_data=hero.exp)
            hero.next_level = False

        if hero.end_game:
            if stat_dict['completion_time'] == 0:
                time_value = (pygame.time.get_ticks() - start_time) // 1000
            else:
                time_value = stat_dict['completion_time']
            scores = int(1 / time_value * 50000 + hero.exp * 2 + hero.health_bar.hp * 10)
            its_time_to_go(screen, scores)
            send_patch_request(username, final_score, scores)
            sys.exit()

        camera.update(hero)
        for e in entities:
            if isinstance(e, Lava):
                e.animate()
            if not isinstance(e, Player):  # Отрисовываем телепорт перед героем
                screen.blit(e.image, camera.apply(e))

        screen.blit(hero.image, camera.apply(hero))
        hero.update(left, right, up, platforms, attack, screen, username)
        for mvp in moving_platforms:
            mvp.update(len(moving_platforms))
        monsters.update(platforms)
        status.update(hero, pygame.time.get_ticks() - start_time)
        attack_effect.update(attack, platforms, hero)
        hero.draw_health_bar(screen)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()
