import unittest
import pygame
from player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        size = 30
        x = 100
        y = 200
        screen = pygame.Surface((800, 600))  # Создаем поверхность для экрана
        username = "TestPlayer"
        exp = 0

        self.player = Player(x, y, screen, username, exp)


    def test_move_left(self):
        initial_x = self.player.rect.x

        # Simulate moving left
        self.player.update(left=True, right=False, up=False, platforms=[], attack=False, screen=None, username=None)

        # Check if the player has moved left
        self.assertLess(self.player.rect.x, initial_x)

    def test_move_right(self):
        initial_x = self.player.rect.x

        # Simulate moving right
        self.player.update(left=False, right=True, up=False, platforms=[], attack=False, screen=None, username=None)

        # Check if the player has moved right
        self.assertGreater(self.player.rect.x, initial_x)

    def test_attack(self):
        initial_image = self.player.image

        # Simulate an attack
        self.player.update(left=False, right=False, up=False, platforms=[], attack=True, screen=None, username=None)

        # Check if the image has changed during the attack
        self.assertNotEqual(initial_image, self.player.image)



    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()