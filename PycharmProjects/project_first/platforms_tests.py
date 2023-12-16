import unittest
import pygame
from blocks import Platform, MovingPlatform, Lava, Teleport, Thorns
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
class TestMovingPlatform(unittest.TestCase):

    def setUp(self):
        x = 100
        y = 200
        image_path = "images/blocks/transform_platform.png"
        start_x = 100
        end_x = 300
        speed = 5
        self.moving_platform = MovingPlatform(x, y, image_path, start_x, end_x, speed)

    def test_moving_platform_initialization(self):
        self.assertEqual(self.moving_platform.rect.x, 100)
        self.assertEqual(self.moving_platform.rect.y, 200)
        self.assertEqual(self.moving_platform.start_x, 100)
        self.assertEqual(self.moving_platform.end_x, 300)
        self.assertEqual(self.moving_platform.speed, 5)
        self.assertEqual(self.moving_platform.direction, 1)

    def test_set_hero(self):
        hero = pygame.sprite.Sprite()
        self.moving_platform.set_hero(hero)
        self.assertEqual(self.moving_platform.hero, hero)


class TestLava(unittest.TestCase):

    def setUp(self):
        x = 100
        y = 200
        images = ['images/lava/lava1.png',
                  'images/lava/lava2.png',
                  'images/lava/lava3.png',
                  'images/lava/lava4.png']
        self.lava = Lava(x, y, images)



class TestTeleport(unittest.TestCase):

    def setUp(self):
        x = 100
        y = 200
        image_path = 'images/teleport.png'
        self.teleport = Teleport(x, y, image_path)

    def test_teleport_initialization(self):
        self.assertEqual(self.teleport.rect.x, 100)
        self.assertEqual(self.teleport.rect.y, 200)
        self.assertEqual(self.teleport.image.get_size(), (PLATFORM_WIDTH, PLATFORM_HEIGHT))

class TestThorns(unittest.TestCase):

    def setUp(self):
        x = 100
        y = 200
        image_path = 'objects/torch.png'
        self.thorns = Thorns(x, y, image_path)

    def test_thorns_initialization(self):
        self.assertEqual(self.thorns.rect.x, 100)
        self.assertEqual(self.thorns.rect.y, 200)
        self.assertEqual(self.thorns.image.get_size(), (32, 16))

if __name__ == '__main__':
    unittest.main()