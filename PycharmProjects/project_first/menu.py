import pygame as pg
from pygame import *
import sys
import requests
from settings import *


def send_post_request(username, password):
    url = "http://localhost:8000/api/player_info/"
    data = {"login": username, "password": password}
    response = requests.post(url, data=data)
    print(response.text)


def menuFunc():
    reg = False
    clock = pygame.time.Clock()
    background_image = pg.image.load('images/Background.png')
    scaled_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    while not reg:
        screen.blit(scaled_image, (0, 0))
        font_path = 'fonts/thin_pixel-7.ttf'
        font = pg.font.Font(font_path, 36)

        login_button_rect = draw_rect(screen, 35, 20, 30, 10)
        register_button_rect = draw_rect(screen, 35, 40, 30, 10)

        login_text = font.render("Войти", True, (0, 0, 0))
        register_text = font.render("Рейтинг", True, (0, 0, 0))
        login_text_rect = login_text.get_rect()
        register_text_rect = register_text.get_rect()
        login_text_rect.center = ((login_button_rect.right + login_button_rect.left) // 2,
                                  (login_button_rect.bottom + login_button_rect.top) // 2)
        register_text_rect.center = ((register_button_rect.right + register_button_rect.left) // 2,
                                     (register_button_rect.bottom + register_button_rect.top) // 2)
        screen.blit(login_text, login_text_rect)
        screen.blit(register_text, register_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if login_button_rect.collidepoint(event.pos):
                    print("Нажата кнопка 'Войти'")
                    menu_reg_func(font, screen)
                    reg = True
                elif register_button_rect.collidepoint(event.pos):
                    print("Нажата кнопка 'Рейтинг'")
        pygame.display.flip()
        clock.tick(60)

    return reg


def draw_rect(screen, x, y, width, height, clr=(255, 255, 255), border=20, border_width=0):
    window_x = (WINDOW_WIDTH * x) // 100
    window_y = (WINDOW_HEIGHT * y) // 100
    window_width = (WINDOW_WIDTH * width) // 100
    window_height = (WINDOW_HEIGHT * height) // 100
    n_rect = pg.Rect(window_x, window_y, window_width, window_height)
    pygame.draw.rect(screen, clr, n_rect, border_radius=border, width=border_width)
    return n_rect


def menu_reg_func(font, screen):
    input_active = True
    reg_window = draw_rect(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128))

    # треба настроить прозрачность
    name_window = draw_rect(screen, 30, 30, 40, 10, clr=(0, 0, 0), border_width=2)
    pass_window = draw_rect(screen, 30, 45, 40, 10, clr=(0, 0, 0), border_width=2)
    init_window = draw_rect(screen, 45, 60, 10, 5, clr=(255, 0, 0), border_width=3)

    name_text = font.render("Логин: ", True, (200, 200, 200))
    pass_text = font.render("Пароль: ", True, (200, 200, 200))
    init_text = font.render("Играть", True, (0, 0, 0))
    # здесь задаем тексты логина пароля
    name_text_rect = name_text.get_rect()
    pass_text_rect = pass_text.get_rect()
    init_text_rect = init_text.get_rect()
    name_text_rect.center = ((name_window.right + name_window.left) // 2,
                             (name_window.bottom + name_window.top) // 2)
    pass_text_rect.center = ((pass_window.right + pass_window.left) // 2,
                             (pass_window.bottom + pass_window.top) // 2)
    init_text_rect.center = ((init_window.right + init_window.left + 2) // 2,
                             (init_window.bottom + init_window.top - 6) // 2)

    screen.blit(name_text, name_text_rect)
    screen.blit(pass_text, pass_text_rect)
    screen.blit(init_text, init_text_rect)
    # для активации поля ввода

    active_name = False
    active_pass = False
    text_name = ''
    text_pass = ''

    while input_active:
        pygame.font.init()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if name_window.collidepoint(event.pos):
                    active_name = not active_name
                    active_pass = False
                    pygame.draw.rect(screen, (0, 255, 0), name_window, 2, border_radius=20)
                    pygame.draw.rect(screen, (0, 0, 0), pass_window, 2, border_radius=20)
                elif pass_window.collidepoint(event.pos):
                    active_pass = not active_pass
                    active_name = False
                    pygame.draw.rect(screen, (0, 255, 0), pass_window, 2, border_radius=20)
                    pygame.draw.rect(screen, (0, 0, 0), name_window, 2, border_radius=20)
                elif init_window.collidepoint(event.pos):
                    if text_name != '' and text_pass != '':
                        send_post_request(text_name, text_pass)
                        input_active = False

            elif event.type == pygame.KEYDOWN:
                if active_name:
                    text_name = text_bar_updating(screen, event, font, name_window, text_name, name_text_rect)
                elif active_pass:
                    text_pass = text_bar_updating(screen, event, font, pass_window, text_pass, pass_text_rect)

                if text_name != '' and text_pass != '':
                    pygame.draw.rect(screen, (0, 255, 0), init_window, 3, border_radius=20)
        pygame.display.flip()


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
