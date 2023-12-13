import pygame
import pytest
import sys
from settings import *
from menu import death_screen


# def test_death_screen_positive():
#     pygame.init()
#     screen = pygame.display.set_mode((1080, 720))
#     pygame.display.set_caption("Test Game")
#     pygame.mouse.set_visible(False)
#
#     try:
#         death_screen(screen)
#     except SystemExit:

def test_death_screen_negative():
    pygame.init()
    screen = pygame.display.set_mode((-1, -1))
    pygame.display.set_caption("Test Game")
    pygame.mouse.set_visible(False)

    def custom_screen_creator():
        # Этот код не должен вызывать исключение pygame.error
        return pygame.display.set_mode((800, 600))

    with pytest.raises(pygame.error) as e:
        death_screen(custom_screen_creator)

    assert str(e.value) == "Cannot set negative sized display mode"