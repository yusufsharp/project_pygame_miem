import pygame
import pytest
import sys
from settings import *
from menu import *

# Используйте фикстуру pytest для создания окна Pygame
@pytest.fixture
def pygame_window():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    yield window
    pygame.quit()


def test_draw_rect_color_true(pygame_window):
    draw_rect(pygame_window, 5, 10, 5, 10, clr=(80, 81, 82))
    pygame.display.flip()
    color_at_rect = pygame_window.get_at((int(WINDOW_WIDTH * (6 / 100)), int(WINDOW_HEIGHT * (11 / 100))))[:3]
    assert color_at_rect == (80, 81, 82)


def test_draw_rect_color(pygame_window):

    draw_rect(pygame_window, 5, 10, 5, 10, clr=(80, 81, 82))
    pygame.display.flip()
    color_at_rect = pygame_window.get_at((int(WINDOW_WIDTH * (6 / 100)), int(WINDOW_HEIGHT * (11 / 100))))[:3]
    assert color_at_rect == (80, 81, 82)


def test_text_in_bar_text_height_true(pygame_window):
    lol_rect = draw_rect(pygame_window, 5, 10, 5, 10, clr=(200, 200, 200))
    lol_font = pg.font.Font('fonts/thin_pixel-7.ttf', 10)
    lol_text_rect = print_text_in_bar(pygame_window, lol_font, 'aboba', lol_rect)
    assert lol_text_rect.height == 10


def test_text_in_bar_text_height_false(pygame_window):
    lol_rect = draw_rect(pygame_window, 5, 10, 5, 10, clr=(200, 200, 200))
    lol_font = pg.font.Font('fonts/thin_pixel-7.ttf', 5)
    lol_text_rect = print_text_in_bar(pygame_window, lol_font, 'aboba', lol_rect)
    assert lol_text_rect.height != 10
