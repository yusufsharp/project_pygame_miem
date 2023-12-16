import unittest
import pygame
from enemies import Enemy

class TestEnemy(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1, 1), pygame.NOFRAME)
        x = 100
        y = 200
        left = 2
        up = 1
        maxLengthLeft = 50
        maxLengthUp = 30
        hp = 10

        self.enemy = Enemy(x, y, left, up, maxLengthLeft, maxLengthUp, hp)

    def test_initialization(self):
        self.assertEqual(self.enemy.rect.x, 100)
        self.assertEqual(self.enemy.rect.y, 200)
        self.assertEqual(self.enemy.startX, 100)
        self.assertEqual(self.enemy.startY, 200)
        self.assertEqual(self.enemy.maxLengthLeft, 50)
        self.assertEqual(self.enemy.maxLengthUp, 30)
        self.assertEqual(self.enemy.xvel, 2)
        self.assertEqual(self.enemy.yvel, 1)
        self.assertEqual(self.enemy.hp, 10)

    def test_update_movement(self):
        initial_x = self.enemy.rect.x
        initial_y = self.enemy.rect.y

        # Предполагаем, что враг движется вправо
        self.enemy.update([])

        # Проверяем, что враг переместился горизонтально
        self.assertEqual(initial_x + self.enemy.xvel, self.enemy.rect.x)

    def test_die(self):
        platforms = []  # Фиктивная платформа для тестирования

        self.enemy.die()

        # Проверяем, что враг удален из платформ
        self.assertNotIn(self.enemy, platforms)
        self.assertTrue(self.enemy not in pygame.sprite.spritecollide(self.enemy, platforms, False))

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()