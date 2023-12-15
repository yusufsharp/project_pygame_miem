import pygame as pg
from pygame import *
import sys
import requests
from settings import *
import math
import json
import random


def send_post_request(username, password):
    """
        Отправляет POST-запрос с предоставленными учетными данными нового пользователя.
        Сервер регистрирует его в базу данных

        :param username: Имя пользователя для отправки в запросе.
        :type username: str
        :param password: Пароль для отправки в запросе.
        :type password: str
        :return: Имя пользователя, отправленное в запросе.
        :rtype: str
        :raises requests.exceptions.RequestException: В случае ошибки при отправке POST-запроса.
    """
    url = "https://zxces.pythonanywhere.com/myapp/api/player_info/"
    data = {"login": username, "password": password, "achieves": {
        'experience': 0,
        'health': 0,
        'points': 0,
        'completion_time': 0
    }}
    response = requests.post(url, json=data)
    print(response.text)
    return username


def send_get_request(username, password):
    """
        Выполняет GET-запрос для получения информации об игроке по указанному имени пользователя.

        :param username: Имя пользователя, для которого выполняется запрос.
        :type username: str
        :param password: Пароль, используемый в запросе для аутентификации.
        :type password: str
        :return: True, если игрок найден, False в противном случае.
        :rtype: bool
        :raises requests.exceptions.RequestException: В случае ошибки при отправке GET-запроса.

        Если статус ответа равен 200, функция выводит информацию о найденном игроке и возвращает True.
        Если статус ответа равен 404, функция выводит сообщение о том, что игрок не найден, и возвращает False.
        В случае любой другой ошибки, функция выводит сообщение об ошибке с указанием статуса
            и текста ответа, и возвращает False.
        """
    url = f"https://zxces.pythonanywhere.com/api/player_info/{username}"
    params = {"login": username, "password": password}
    # start_time = pg.time.get_ticks()
    response = requests.get(url, params=params)
    # print('Время:', pg.time.get_ticks()-start_time)
    if response.status_code == 200:
        player_info = response.json()
        print("Игрок найден. Информация о игроке:", player_info)
        print(response.text)
        return True
    elif response.status_code == 404:
        print("Игрок не найден.")
        print(response.text)
        return False
    else:
        print(f"Произошла ошибка: {response.status_code}, {response.text}")
        return False


def register_request(username, password):
    """
        Выполняет запрос на регистрацию игрока по указанному имени пользователя и паролю на сгенерированную ссылку.

        :param username: Имя пользователя для регистрации.
        :type username: str
        :param password: Пароль для регистрации.
        :type password: str
        :return: Кортеж (True, username) в случае успешной регистрации, False в противном случае.
        :rtype: tuple(bool, str)
        :raises requests.exceptions.RequestException: В случае ошибки при отправке GET-запроса.

        Если статус ответа равен 200, функция выводит информацию о зарегистрированном игроке
            и возвращает кортеж (True, username).
        В случае любой другой ошибки, функция выводит сообщение об ошибке с указанием статуса
            и текста ответа, и возвращает False.
        """
    url = f"https://zxces.pythonanywhere.com/register/{username}/{password}"  # генерит ссылку логин и пароль
    response = requests.get(url)
    if response.status_code == 200:
        player_info = response.json()
        print("Игрок зарегестрирован", player_info)
        print(response.text)
        # send_patch_request(username, 'experience', 101)
        return True, username
    else:
        print(f"Неверный пароль: {response.status_code}, {response.text}")
        return False, ''


def send_patch_request(username, achieve_type, type_value, secure_key=SECURE_KEY):
    """
        Выполняет PATCH-запрос для обновления достижения игрока по указанному имени пользователя на
        сгенерированную ссылку.

        :param username: Имя пользователя, для которого выполняется запрос.
        :type username: str
        :param achieve_type: Тип достижения, которое необходимо обновить (например, 'experience').
        :type achieve_type: str
        :param type_value: Новое значение для достижения.
        :type type_value: int
        :param secure_key: Ключ безопасности (по умолчанию используется значение из глобальной переменной SECURE_KEY).
        :type secure_key: str
        :return: None

        Результат выполнения запроса выводится на экран в виде статуса и JSON-данных ответа.
        """
    url = f'https://zxces.pythonanywhere.com/update-achieves/{username}/{achieve_type}/{type_value}/'
    params = {'key': secure_key}
    response = requests.patch(url, params=params)
    print(response.status_code)
    print(response.json())
    return


def stat_request(username):
    """
        Получение статистики и достижений игрока из внешнего API.

        :param username: Имя пользователя игрока, для которого необходимо получить информацию.
        :type username: str
        :return: Словарь, содержащий статистику и достижения игрока. Возвращает пустой словарь в случае ошибки запроса.
        :rtype: dict
        """
    url = f"https://zxces.pythonanywhere.com/api/player_info/{username}"

    response = requests.get(url)
    if response.status_code == 200:
        player_info = json.loads(response.text)
        stats = player_info['achieves']
        del stats['id']
        print("Игрок найден. Информация о игроке:", stats)
        return stats
    else:
        print(f"Произошла ошибка: {response.status_code}, {response.text}")
        return dict()


def menu_func():
    """
        Отображает главное меню игры.

        :return: (reg, username), где reg - флаг прохождения регистрации, username - имя пользователя.
        :rtype: tuple(bool, str)
        """
    reg = False  # отвечает за отображение всего меню
    username = 'АНОНИМУС'
    clock = pygame.time.Clock()  # фпс
    background_image = pg.image.load('images/Background.png')
    scaled_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # подгоняем изображение
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_image, (0, 0))  # отображаем изображение
    font_menu = pg.font.Font('fonts/thin_pixel-7.ttf', 36)
    animate(screen, 35, 20, 30, 10)  # анимация появления логин
    login_button_rect = draw_rect(screen, 35, 20, 30, 10)
    print_text_in_bar(screen, font_menu, 'Войти', login_button_rect, clr=(0, 0, 0))
    animate(screen, 35, 40, 30, 10)  # анимация появления рейтинг
    register_button_rect = draw_rect(screen, 35, 40, 30, 10)
    print_text_in_bar(screen, font_menu, 'Рейтинг', register_button_rect, clr=(0, 0, 0))

    login_rating_active = False
    while not reg:
        # главный цикл отображает запускает все остальное
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif menu_event.type == pg.MOUSEBUTTONDOWN:
                if login_button_rect.collidepoint(menu_event.pos) and not login_rating_active:
                    login_rating_active = True
                    print("Нажата кнопка 'Войти'")
                    username = menu_reg_func(font_menu, screen, username)
                    darken_screen(screen)
                    reg = True
                elif register_button_rect.collidepoint(menu_event.pos) and not login_rating_active:
                    login_rating_active = True
                    print("Нажата кнопка 'Рейтинг'")
                    menu_rating_func(font_menu, screen)
        pygame.display.flip()
        clock.tick(60)

    return reg, username


def menu_reg_func(some_font, screen, username):
    """
        Отображает окно регистрации и обработку ввода пользователя.

        :param some_font: Шрифт для текста.
        :type some_font: pygame.font.Font
        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param username: Текущее имя пользователя.
        :type username: str
        :return: Имя пользователя после регистрации.
        :rtype: str
        """
    input_active = True  # переменная которая отвечает за прогонку меню окна регистрации
    animate(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128), duration=300)
    draw_rect(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128))

    # треба настроить прозрачность
    name_window = draw_rect(screen, 30, 30, 40, 10, clr=(0, 0, 0), border_width=2)
    pass_window = draw_rect(screen, 30, 45, 40, 10, clr=(0, 0, 0), border_width=2)
    init_window = draw_rect(screen, 45, 60, 10, 5, clr=(255, 0, 0), border_width=3)
    name_text_rect = print_text_in_bar(screen, some_font, "Логин: ", name_window)
    pass_text_rect = print_text_in_bar(screen, some_font, "Пароль: ", pass_window)
    print_text_in_bar(screen, some_font, "Играть", init_window, right_pos=2, bottom_pos=-6, clr=(0, 0, 0))

    active_name = False  # нажатие на окно логина
    active_pass = False  # нажатие на окно пароля
    text_name = ''  # сам текст
    text_pass = ''

    while input_active:
        pygame.font.init()

        for reg_event in pygame.event.get():  # анализ клавиатуры
            if reg_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif reg_event.type == pygame.MOUSEBUTTONDOWN:
                if name_window.collidepoint(reg_event.pos):
                    active_name = True
                    active_pass = False
                    pygame.draw.rect(screen, (0, 255, 0), name_window, 2, border_radius=20)  # меняет цвет рамки логин
                    pygame.draw.rect(screen, (0, 0, 0), pass_window, 2, border_radius=20)  # меняет цвет пароль
                elif pass_window.collidepoint(reg_event.pos):
                    active_pass = True
                    active_name = False
                    pygame.draw.rect(screen, (0, 255, 0), pass_window, 2, border_radius=20)
                    pygame.draw.rect(screen, (0, 0, 0), name_window, 2, border_radius=20)
                elif init_window.collidepoint(reg_event.pos):  # нажатие на кнопку играть
                    if text_name != '' and text_pass != '':  # не пустые рамки с текстом
                        pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                        animate(screen, 45, 60, 10, 5, clr=(0, 255, 0))  # зеленый батон загрузки
                        user_exists = send_get_request(text_name, text_pass)  # проверка на регу игрока
                        if not user_exists:
                            pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                            animate(screen, 45, 60, 10, 5, clr=(200, 200, 200))  # серый батон загрузки
                            username = send_post_request(text_name, text_pass)  # передает данные для реги
                            print('Игрок проходит регистрацию')
                            input_active = False  # закончили арку меню
                        else:
                            auth, username = register_request(text_name, text_pass)  # проверка пароля
                            if not auth:
                                pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                                animate(screen, 45, 60, 10, 5, clr=(255, 0, 0))  # красный батон загрузки
                                error_rect = draw_rect(screen, 35, 20, 30, 10)
                                print_text_in_bar(screen, some_font, 'Неверный пароль!', error_rect, clr=(255, 0, 0))
                            else:
                                pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                                animate(screen, 45, 60, 10, 5, clr=pygame.Color('dodgerblue2'))  # синий батон загрузки
                                print('Добро пожаловать!!!')
                                input_active = False

            elif reg_event.type == pygame.KEYDOWN:  # любая клавиша текста
                if active_name:  # функция обновляет и центрирует текст
                    text_name = text_bar_updating(screen, reg_event, some_font, name_window, text_name, name_text_rect)
                elif active_pass:
                    text_pass = text_bar_updating(screen, reg_event, some_font, pass_window, text_pass, pass_text_rect)

                if text_name != '' and text_pass != '':
                    pygame.draw.rect(screen, (255, 255, 255), init_window, border_radius=20)  # делает зеленую рамку
                    print_text_in_bar(screen, some_font, "Играть", init_window, right_pos=2,
                                      bottom_pos=-6, clr=(0, 0, 0))
                    pygame.draw.rect(screen, (0, 255, 0), init_window, 3, border_radius=20)
        pygame.display.flip()
    return username


def draw_rect(screen, x, y, width, height, clr=(255, 255, 255), border=20, border_width=0):
    """
        Рисует прямоугольник на экране.

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param x: Позиция по горизонтали в процентах от ширины экрана.
        :type x: float
        :param y: Позиция по вертикали в процентах от высоты экрана.
        :type y: float
        :param width: Ширина прямоугольника в процентах от ширины экрана.
        :type width: float
        :param height: Высота прямоугольника в процентах от высоты экрана.
        :type height: float
        :param clr: Цвет прямоугольника в формате RGB.
        :type clr: tuple(int, int, int)
        :param border: Радиус скругления углов прямоугольника.
        :type border: int
        :param border_width: Ширина границы прямоугольника.
        :type border_width: int
        :return: Объект Rect, представляющий координаты и размеры прямоугольника.
        :rtype: pygame.Rect
        """
    window_x = (WINDOW_WIDTH * x) // 100
    window_y = (WINDOW_HEIGHT * y) // 100
    window_width = (WINDOW_WIDTH * width) // 100
    window_height = (WINDOW_HEIGHT * height) // 100
    n_rect = pg.Rect(window_x, window_y, window_width, window_height)
    pygame.draw.rect(screen, clr, n_rect, border_radius=border, width=border_width)
    return n_rect


def print_text_in_bar(screen, some_font, text, bar, right_pos=0, bottom_pos=0, clr=(200, 200, 200)):
    """
        Отображает текст внутри прямоугольной области по центру.

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param some_font: Шрифт для текста.
        :type some_font: pygame.font.Font
        :param text: Текст, который нужно отобразить.
        :type text: str
        :param bar: Прямоугольная область, в которой будет отображен текст.
        :type bar: pygame.Rect
        :param right_pos: Позиция текста от правого края прямоугольной области.
        :type right_pos: int
        :param bottom_pos: Позиция текста от нижнего края прямоугольной области.
        :type bottom_pos: int
        :param clr: Цвет текста в формате RGB.
        :type clr: tuple(int, int, int)
        :return: Объект Rect, представляющий координаты и размеры текста.
        :rtype: pygame.Rect
        """
    bar_text = some_font.render(f"{text}", True, clr)

    bar_text_rect = bar_text.get_rect()
    bar_text_rect.center = ((bar.right + bar.left + right_pos) // 2,
                            (bar.bottom + bar.top + bottom_pos) // 2)

    screen.blit(bar_text, bar_text_rect)
    return bar_text_rect


def text_bar_updating(screen, some_event, some_font, window, text, text_rect):
    """
        Обновляет и центрирует текст внутри прямоугольной области при вводе.

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param some_event: Объект события клавиатуры.
        :type some_event: pygame.event.Event
        :param some_font: Шрифт для текста.
        :type some_font: pygame.font.Font
        :param window: Прямоугольная область, в которой отображается текст.
        :type window: pygame.Rect
        :param text: Текущий текст.
        :type text: str
        :param text_rect: Объект Rect, представляющий координаты и размеры текста.
        :type text_rect: pygame.Rect
        :return: Обновленный текст.
        :rtype: str
    """
    pygame.draw.rect(screen, (255, 255, 255), window)
    pygame.draw.rect(screen, (0, 255, 0), window, 2, border_radius=20)
    if some_event.key == pygame.K_RETURN:
        text = ""
    elif some_event.key == pygame.K_BACKSPACE:
        text = text[:-1]
    else:
        text += some_event.unicode
    text_surface = some_font.render(text, True, pygame.Color('dodgerblue2'))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = ((text_rect.right + text_rect.left) // 2,
                                (text_rect.bottom + text_rect.top) // 2)
    screen.blit(text_surface, text_surface_rect)

    return text


def animate(screen, x, y, width, height, clr=(255, 255, 255), border=20, border_width=0, duration=250):
    """
        Анимирует появление прямоугольной области на экране. Нелинейная анимация от корня куба

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param x: Позиция по горизонтали в процентах от ширины экрана.
        :type x: float
        :param y: Позиция по вертикали в процентах от высоты экрана.
        :type y: float
        :param width: Ширина прямоугольника в процентах от ширины экрана.
        :type width: float
        :param height: Высота прямоугольника в процентах от высоты экрана.
        :type height: float
        :param clr: Цвет прямоугольника в формате RGB.
        :type clr: tuple(int, int, int)
        :param border: Радиус скругления углов прямоугольника.
        :type border: int
        :param border_width: Ширина границы прямоугольника.
        :type border_width: int
        :param duration: Длительность анимации в миллисекундах.
        :type duration: int
        :return: None
        """
    start_time = pg.time.get_ticks()
    while True:
        elapsed_time = pg.time.get_ticks() - start_time
        if elapsed_time >= duration:
            break

        progress = (elapsed_time / duration) ** (1 / 3)  # нелинейное отображение корнем куба

        window_x = (WINDOW_WIDTH * (x + (width * (1 - progress) / 2))) // 100
        window_y = (WINDOW_HEIGHT * y) // 100

        window_width = int((WINDOW_WIDTH * width) / 100 * progress)
        window_height = (WINDOW_HEIGHT * height) // 100
        n_rect = pg.Rect(window_x, window_y, window_width, window_height)
        pygame.draw.rect(screen, clr, n_rect, border_radius=border, width=border_width)
        for some_event in pg.event.get():
            if some_event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.time.Clock().tick(60)  # фпс
        pygame.display.flip()  # обновление экрана


def darken_screen(screen, duration=3000):
    """
        Затемняет экран с и выводит название игры и увеличивающийся круг посредством анимации.
        В качестве главной заставки игры.

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :param duration: Длительность анимации в миллисекундах.
        :type duration: int
        :return: None
        """
    overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))  # задаем черный цвет, чистим экран
    alpha = 0
    start_time = pg.time.get_ticks()

    while alpha <= 255:
        elapsed_time = pg.time.get_ticks() - start_time
        if elapsed_time >= duration:
            break
        progress = math.sin((elapsed_time / duration) * math.pi / 2)  # нелинейное отображение синусом

        some_font = pg.font.Font('fonts/thin_pixel-7.ttf', int(32 + progress * 404))  # изменяем размер шрифта
        alpha = int(progress * 255)
        overlay.set_alpha(alpha)  # просвет на поверхность
        radius = progress * WINDOW_WIDTH
        alpha = int((1 - progress) * 255)
        screen.blit(overlay, (0, 0))  # наложение затемненной поверхности на экран
        pg.draw.circle(overlay, (200, 0, 0, alpha), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), int(radius))
        overlay_rect = overlay.get_rect()
        print_text_in_bar(screen, some_font, "Buhs' Hero", overlay_rect, clr=(255, 255, 255))

        pg.display.flip()

        for some_event in pg.event.get():
            if some_event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.time.Clock().tick(60)


def menu_rating_func(some_font, screen):
    """
        Отображает рейтинг игроков с использованием анимации. Сначала отправляет GET-запрос на сервер для
        получения базы данных. Потом выводит ее в форме таблицы. Листать таблицу можно нажимая на клавиши PgUp
        и PgDown.

        :param some_font: Шрифт для текста.
        :type some_font: pygame.font.Font
        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :return: None
        """
    animate(screen, 34, 40, 32, 10, clr=pygame.Color('dodgerblue2'))
    screen.fill((255, 255, 255))
    db_json = requests.get("https://zxces.pythonanywhere.com/api/player_info/").text
    db = json.loads(db_json)
    menu_rating = True

    for elm in db:
        del elm['password']
        del elm['achieves']['id']
    db = sorted(db, key=lambda item: item['achieves']['points'], reverse=True)
    scroll = 0
    anima = True
    while menu_rating:

        screen.fill((255, 255, 255))
        for some_event in pygame.event.get():
            if some_event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif some_event.type == KEYDOWN:
                if some_event.key == K_UP:
                    scroll -= 1
                elif some_event.key == K_DOWN:
                    scroll += 1
        scroll = abs(scroll % len(db))
        headers = ['Name', 'Experience', 'Health', 'Points', 'Speedrun']
        i = 25
        for elm in headers:
            cell_achieve = draw_rect(screen, i, 10, 10, 5, border=5, border_width=2, clr=(0, 0, 0))
            print_text_in_bar(screen, some_font, elm, cell_achieve, clr=pygame.Color('dodgerblue2'))
            i += 10

        j = 20
        for k in range(scroll, len(db)):
            i = 25
            cell_login = draw_rect(screen, i, j, 10, 5, border=5, border_width=2, clr=(0, 0, 0))
            print_text_in_bar(screen, some_font, db[k]['login'], cell_login, clr=(0, 0, 0))
            i += 10
            for achieve in db[k]['achieves'].values():
                if anima and k < 12:
                    animate(screen, i, j, 10, 5, clr=(0, 0, 0), border=5, border_width=2, duration=5)
                cell_achieve = draw_rect(screen, i, j, 10, 5, border=5, border_width=2, clr=(0, 0, 0))
                print_text_in_bar(screen, some_font, achieve, cell_achieve, clr=(0, 0, 0))
                i += 10
            j += 6
        anima = False
        pygame.display.flip()


def death_screen(screen):
    """
        Отображает экран смерти персонажа с возможностью возрождения и обновления данных игрока.
        Анимация представляет нелинейную функцию появления крови (корень 5-й степени), затем
        подергивания вследствие генерации случайных координат каждый момент времени.

        :param screen: Объект экрана Pygame.
        :type screen: pygame.Surface
        :return: None
        """
    some_font = pg.font.Font('fonts/thin_pixel-7.ttf', 320)
    original_image = pygame.image.load("images/blood.png")
    image_rect = original_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    duration = 500
    start_time = pg.time.get_ticks()
    respawn_rect = draw_rect(screen, 30, 70, 40, 10, clr=(255, 0, 0), border_width=8)
    flag_return = False
    # Главный цикл игры
    while True:
        elapsed_time = pg.time.get_ticks() - start_time

        for some_event in pygame.event.get():
            if some_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if elapsed_time < duration:
            progress = 3 - 2.5 * (elapsed_time / duration) ** (1 / 5)
            # Уменьшение размера изображения
            scaled_image = pygame.transform.scale(original_image, (
                int(image_rect.width * progress), int(image_rect.height * progress)))
            screen.fill((0, 0, 0))
            screen.blit(scaled_image, scaled_image.get_rect(center=image_rect.center))
        else:
            scaled_image = pygame.transform.scale(original_image, (
                int(image_rect.width * 0.5), int(image_rect.height * 0.5)))
            screen.fill((0, 0, 0))
            screen.blit(scaled_image, scaled_image.get_rect(center=((WINDOW_WIDTH + random.randint(-50, 50)) // 2,
                                                                    (WINDOW_HEIGHT + random.randint(-50, 50)) // 2)))
            print_text_in_bar(screen, some_font, "ТЫ МЕРТВ",
                              screen.get_rect(center=((WINDOW_WIDTH + random.randint(-10, 10)) // 2,
                                                      (WINDOW_HEIGHT + random.randint(-10, 10)) // 2)),
                              clr=(200, 200, 200))

            draw_rect(screen, 30, 70, 40, 10, clr=(255, 0, 0), border_width=8)
            print_text_in_bar(screen, pg.font.Font('fonts/thin_pixel-7.ttf', 60),
                              'Возродиться', respawn_rect, bottom_pos=-5)
            for some_event in pygame.event.get():
                if some_event.type == pg.MOUSEBUTTONDOWN:
                    if respawn_rect.collidepoint(some_event.pos):
                        # какая то функция...
                        flag_return = True
                        return
        if flag_return:
            return True

        pygame.display.flip()
        pygame.time.Clock().tick(60)
