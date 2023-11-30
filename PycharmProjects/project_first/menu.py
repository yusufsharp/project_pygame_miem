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

        button_width = 300
        button_height = 70
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
    text = ''
    reg_window = draw_rect(screen, 20, 20, 60, 50, clr=(255, 255, 255, 128))

    # треба настроить прозрачность
    name_window = draw_rect(screen, 30, 30, 40, 10, clr=(0, 0, 0), border_width=2)
    pass_window = draw_rect(screen, 30, 45, 40, 10, clr=(0, 0, 0), border_width=2)

    name_text = font.render("Логин: ", True, (200, 200, 200))
    pass_text = font.render("Пароль: ", True, (200, 200, 200))

    name_text_rect = name_text.get_rect()
    pass_text_rect = pass_text.get_rect()
    name_text_rect.center = ((name_window.right + name_window.left) // 2,
                             (name_window.bottom + name_window.top) // 2)
    pass_text_rect.center = ((pass_window.right + pass_window.left) // 2,
                             (pass_window.bottom + pass_window.top) // 2)
    screen.blit(name_text, name_text_rect)
    screen.blit(pass_text, pass_text_rect)
    while input_active:
        pygame.font.init()
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (200, 200))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # send_post_request(text, '1234')
                    text = ""
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        pygame.display.update()
