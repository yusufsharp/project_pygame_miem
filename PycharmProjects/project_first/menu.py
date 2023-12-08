import pygame as pg
from pygame import *
import sys
import requests
from settings import *
import math


def send_post_request(username, password):
    url = "https://zxces.pythonanywhere.com/myapp/api/player_info/"
    data = {"login": username, "password": password}
    response = requests.post(url, data=data)
    print(response.text)  # берет всю бд по адресу


def send_get_request(username, password):
    url = f"https://zxces.pythonanywhere.com/api/player_info/{username}"
    params = {"login": username, "password": password}
    response = requests.get(url, params=params)
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
    url = f"https://zxces.pythonanywhere.com/register/{username}/{password}"  # генерит ссылку логин и пароль
    response = requests.get(url)
    if response.status_code == 200:
        player_info = response.json()
        print("Игрок зарегестрирован", player_info)
        print(response.text)
        return True
    elif response.status_code == 401:
        print(f"Неверный пароль: {response.status_code}, {response.text}")
        return False


def menuFunc():
    reg = False  # отвечает за отображение всего меню
    clock = pygame.time.Clock()  # фпс
    background_image = pg.image.load('images/Background.png')
    scaled_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))  # подгоняем изображение
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_image, (0, 0))  # отображаем изображение
    font = pg.font.Font('fonts/thin_pixel-7.ttf', 36)
    animate(screen, 35, 20, 30, 10)  # анимация появления логин
    login_button_rect = draw_rect(screen, 35, 20, 30, 10)
    print_text_in_bar(screen, font, 'Войти', login_button_rect, clr=(0, 0, 0))
    animate(screen, 35, 40, 30, 10)  # анимация появления рейтинг
    register_button_rect = draw_rect(screen, 35, 40, 30, 10)
    print_text_in_bar(screen, font, 'Рейтинг', register_button_rect, clr=(0, 0, 0))
    while not reg:
        # главный цикл отображает запускает все остальное
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if login_button_rect.collidepoint(event.pos):
                    print("Нажата кнопка 'Войти'")
                    menu_reg_func(font, screen)
                    darken_screen(screen)
                    reg = True
                elif register_button_rect.collidepoint(event.pos):
                    print("Нажата кнопка 'Рейтинг'")
        pygame.display.flip()
        clock.tick(60)

    return reg


def menu_reg_func(font, screen):
    input_active = True  # переменная которая отвечает за прогонку меню окна регистрации
    animate(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128), duration=300)
    draw_rect(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128))

    # треба настроить прозрачность
    name_window = draw_rect(screen, 30, 30, 40, 10, clr=(0, 0, 0), border_width=2)
    pass_window = draw_rect(screen, 30, 45, 40, 10, clr=(0, 0, 0), border_width=2)
    init_window = draw_rect(screen, 45, 60, 10, 5, clr=(255, 0, 0), border_width=3)
    name_text_rect = print_text_in_bar(screen, font, "Логин: ", name_window)
    pass_text_rect = print_text_in_bar(screen, font, "Пароль: ", pass_window)
    print_text_in_bar(screen, font, "Играть", init_window, right_pos=2, bottom_pos=-6, clr=(0, 0, 0))

    active_name = False  # нажатие на окно логина
    active_pass = False  # нажатие на окно пароля
    text_name = ''  # сам текст
    text_pass = ''

    while input_active:
        pygame.font.init()

        for event in pygame.event.get():  # анализ клавиатуры
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if name_window.collidepoint(event.pos):
                    active_name = True
                    active_pass = False
                    pygame.draw.rect(screen, (0, 255, 0), name_window, 2, border_radius=20)  # меняет цвет рамки логин
                    pygame.draw.rect(screen, (0, 0, 0), pass_window, 2, border_radius=20)  # меняет цвет пароль
                elif pass_window.collidepoint(event.pos):
                    active_pass = True
                    active_name = False
                    pygame.draw.rect(screen, (0, 255, 0), pass_window, 2, border_radius=20)
                    pygame.draw.rect(screen, (0, 0, 0), name_window, 2, border_radius=20)
                elif init_window.collidepoint(event.pos):  # нажатие на кнопку играть
                    if text_name != '' and text_pass != '':  # не пустые рамки с текстом
                        pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                        animate(screen, 45, 60, 10, 5, clr=(0, 255, 0))  # зеленый батон загрузки
                        user_exists = send_get_request(text_name, text_pass)  # проверка на регу игрока
                        if not user_exists:
                            pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                            animate(screen, 45, 60, 10, 5, clr=(200, 200, 200))  # серый батон загрузки
                            send_post_request(text_name, text_pass)  # передает данные для реги
                            print('Игрок проходит регистрацию')
                            input_active = False  # закончили арку меню
                        else:
                            auth = register_request(text_name, text_pass)  # проверка пароля
                            if not auth:
                                pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                                animate(screen, 45, 60, 10, 5, clr=(255, 0, 0))  # красный батон загрузки
                                error_rect = draw_rect(screen, 35, 20, 30, 10)
                                print_text_in_bar(screen, font, 'Неверный пароль!', error_rect, clr=(255, 0, 0))
                            else:
                                pygame.draw.rect(screen, (255, 255, 255), init_window)  # отбеливание батона
                                animate(screen, 45, 60, 10, 5, clr=pygame.Color('dodgerblue2'))  # синий батон загрузки
                                print('Добро пожаловать!!!')
                                input_active = False

            elif event.type == pygame.KEYDOWN:  # любая клавиша текста
                if active_name:  # функция обновляет и центрирует текст
                    text_name = text_bar_updating(screen, event, font, name_window, text_name, name_text_rect)
                elif active_pass:
                    text_pass = text_bar_updating(screen, event, font, pass_window, text_pass, pass_text_rect)

                if text_name != '' and text_pass != '':
                    pygame.draw.rect(screen, (255, 255, 255), init_window, border_radius=20)  # делает зеленую рамку
                    print_text_in_bar(screen, font, "Играть", init_window, right_pos=2, bottom_pos=-6, clr=(0, 0, 0))
                    pygame.draw.rect(screen, (0, 255, 0), init_window, 3, border_radius=20)
        pygame.display.flip()


def draw_rect(screen, x, y, width, height, clr=(255, 255, 255), border=20, border_width=0):
    window_x = (WINDOW_WIDTH * x) // 100
    window_y = (WINDOW_HEIGHT * y) // 100
    window_width = (WINDOW_WIDTH * width) // 100
    window_height = (WINDOW_HEIGHT * height) // 100
    n_rect = pg.Rect(window_x, window_y, window_width, window_height)
    pygame.draw.rect(screen, clr, n_rect, border_radius=border, width=border_width)
    return n_rect


def print_text_in_bar(screen, font, text, bar, right_pos=0, bottom_pos=0, clr=(200, 200, 200)):
    bar_text = font.render(f"{text}", True, clr)

    bar_text_rect = bar_text.get_rect()
    bar_text_rect.center = ((bar.right + bar.left + right_pos) // 2,
                            (bar.bottom + bar.top + bottom_pos) // 2)

    screen.blit(bar_text, bar_text_rect)
    return bar_text_rect


def text_bar_updating(screen, event, font, window, text, text_rect):
    pygame.draw.rect(screen, (255, 255, 255), window)
    pygame.draw.rect(screen, (0, 255, 0), window, 2, border_radius=20)
    if event.key == pygame.K_RETURN:
        text = ""
    elif event.key == pygame.K_BACKSPACE:
        text = text[:-1]
    else:
        text += event.unicode
    text_surface = font.render(text, True, pygame.Color('dodgerblue2'))
    text_surface_rect = text_surface.get_rect()
    text_surface_rect.center = ((text_rect.right + text_rect.left) // 2,
                                (text_rect.bottom + text_rect.top) // 2)
    screen.blit(text_surface, text_surface_rect)

    return text


def animate(screen, x, y, width, height, clr=(255, 255, 255), border=20, border_width=0, duration=150):
    start_time = pg.time.get_ticks()
    while True:
        elapsed_time = pg.time.get_ticks() - start_time
        if elapsed_time >= duration:
            break

        progress = elapsed_time / duration

        window_x = (WINDOW_WIDTH * x) // 100
        window_y = (WINDOW_HEIGHT * y) // 100

        window_width = int((WINDOW_WIDTH * width) / 100 * (progress ** (1 / 3)))  # нелинейное отображение корнем куба
        window_height = (WINDOW_HEIGHT * height) // 100
        n_rect = pg.Rect(window_x, window_y, window_width, window_height)
        pygame.draw.rect(screen, clr, n_rect, border_radius=border, width=border_width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.time.Clock().tick(60)  # фпс
        pygame.display.flip()  # обновление экрана


def darken_screen(screen, duration=3000):
    overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.fill((0, 0, 0))  # задаем черный цвет, чистим экран
    alpha = 0
    start_time = pg.time.get_ticks()

    while alpha <= 255:
        elapsed_time = pg.time.get_ticks() - start_time
        if elapsed_time >= duration:
            break
        progress = math.sin((elapsed_time / duration) * math.pi / 2)  # нелинейное отображение синусом

        font = pg.font.Font('fonts/thin_pixel-7.ttf', int(32 + progress * 404))  # изменяем размер шрифта
        alpha = int(progress * 255)
        overlay.set_alpha(alpha)  # просвет на поверхность
        radius = progress * WINDOW_WIDTH
        alpha = int((1 - progress) * 255)
        screen.blit(overlay, (0, 0))  # наложение затемненной поверхности на экран
        pg.draw.circle(overlay, (200, 0, 0, alpha), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), int(radius))
        overlay_rect = overlay.get_rect()
        print_text_in_bar(screen, font, 'Real Hero', overlay_rect, clr=(255, 255, 255))
        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        pg.time.Clock().tick(60)
