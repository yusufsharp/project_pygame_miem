import pygame as pg
from pygame import *
import sys
import requests
from settings import *


def menuFunc():
    reg = False
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 720
    background_image = pg.image.load('images/Background.png')
    scaled_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(scaled_image, (0, 0))

    button_width = 300
    button_height = 70

    login_button_rect = pg.Rect((WINDOW_WIDTH - button_width) // 2, 200, button_width, button_height)
    register_button_rect = pg.Rect((WINDOW_WIDTH - button_width) // 2, 300, button_width, button_height)
    pg.draw.rect(screen, (200, 200, 200), login_button_rect)
    pg.draw.rect(screen, (200, 200, 200), register_button_rect)
    font = pg.font.Font(None, 36)
    login_text = font.render("Войти", True, (0, 0, 0))
    register_text = font.render("Зарегистрироваться", True, (0, 0, 0))
    screen.blit(login_text, (login_button_rect.x + 110, login_button_rect.y + 25))
    screen.blit(register_text, (register_button_rect.x + 30, register_button_rect.y + 25))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if login_button_rect.collidepoint(event.pos):
                print("Нажата кнопка 'Войти'")
                reg = True
            elif register_button_rect.collidepoint(event.pos):
                print("Нажата кнопка 'Зарегистрироваться'")

    return reg
