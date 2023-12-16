import pygame as pg
from pygame import *
import sys
from settings import *


class Platform(sprite.Sprite):
    """
    Класс, представляющий статичную платформу в игре.

    Атрибуты:
    - image: изображение платформы.
    - rect: прямоугольник, определяющий положение и размеры платформы.

    Методы:
    - __init__: инициализация объекта платформы.
    """
    def __init__(self, x, y, image_path):
        """
          Инициализация объекта платформы.

          Параметры:
          - x, y: координаты верхнего левого угла платформы.
          - image_path: путь к изображению платформы.
          """
        sprite.Sprite.__init__(self)
        self.image = image.load(image_path)
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class MovingPlatform(Platform):
    """
    Класс, представляющий движущуюся платформу в игре.

    Атрибуты:
    - start_x, end_x: начальная и конечная координаты движения платформы по горизонтали.
    - speed: скорость движения платформы.
    - direction: направление движения (1 - вправо, -1 - влево).
    - hero: объект героя.

    Методы:
    - __init__: инициализация объекта движущейся платформы.
    - set_hero: установка объекта героя на платформу.
    - update: обновление состояния платформы.
    """
    def __init__(self, x, y, image_path, start_x, end_x, speed):
        """
         Инициализация объекта движущейся платформы.

         Параметры:
         - x, y: координаты верхнего левого угла платформы.
         - image_path: путь к изображению платформы.
         - start_x, end_x: начальная и конечная координаты движения платформы по горизонтали.
         - speed: скорость движения платформы.
         """
        super().__init__(x, y, image_path)
        self.image = pg.transform.scale(self.image, (200, 32))
        self.rect = Rect(x, y, 200, 32)
        self.start_x = start_x
        self.end_x = end_x
        self.speed = speed
        self.direction = 1  # 1 - right, -1 - left
        self.hero = None

    def set_hero(self, hero):
        """
         Установка объекта героя на платформу.

         Параметры:
         - hero: объект героя.
         """
        self.hero = hero

    def update(self, count_moving_platforms):
        """
         Обновляет состояние движущейся платформы.

         Параметры:
         - count_moving_platforms: количество движущихся платформ на уровне.

         Метод обновляет положение движущейся платформы, меняя ее координаты
         в зависимости от текущего направления и скорости. При достижении края
         платформы меняет направление движения. Если герой находится на движущейся
         платформе, его положение также корректируется.

         """
        self.rect.x += self.direction * self.speed

        if self.rect.right > self.end_x or self.rect.left < self.start_x:
            self.direction *= -1
        if self.hero.on_moving_platform:
            self.hero.rect.x += self.direction * (self.speed // count_moving_platforms)


class Lava(Platform):
    """
       Класс, представляющий лаву в игре.

       Атрибуты:
       - images: список изображений для анимации лавы.
       - image_index: индекс текущего изображения.
       - animation_speed: скорость анимации.
       - animation_timer: таймер анимации.

       Методы:
       - __init__: инициализация объекта лавы.
       - animate: анимация лавы.
       """
    def __init__(self, x, y, images):
        """
        Инициализация объекта лавы.

        Параметры:
        - x, y: координаты верхнего левого угла лавы.
        - images: список путей к изображениям для анимации лавы.
        """
        super().__init__(x, y, images[0])
        self.images = [image.load(image_path) for image_path in images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.animation_speed = 0.2
        self.animation_timer = pg.time.get_ticks()

    def animate(self):
        """Анимация лавы."""
        now = pg.time.get_ticks()
        if now - self.animation_timer > self.animation_speed * 1000:
            self.animation_timer = now
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]


class Teleport(Platform):
    """
    Класс, представляющий телепорт в игре.

    Методы:
    - __init__: инициализация объекта телепорта.
    """
    def __init__(self, x, y, image_path):
        """
                Инициализация объекта телепорта.

                Параметры:
                - x, y: координаты верхнего левого угла телепорта.
                - image_path: путь к изображению телепорта.
                """
        super().__init__(x, y, image_path)
        self.image = pg.image.load(image_path)
        self.image = pg.transform.scale(self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Gate(Platform):
    """
    Класс, представляющий ворота для конца игры.

    Методы:
    - __init__: инициализация объекта ворот.
    """
    def __init__(self, x, y, image_path):
        """
           Инициализация объекта ворот.

           Параметры:
           - x, y: координаты верхнего левого угла ворот.
           - image_path: путь к изображению ворот.
           """
        super().__init__(x, y, image_path)
        self.image = pg.image.load(image_path)
        self.rect = Rect(x, y, 32, 64)


class Thorns(Platform):
    """
    Класс, представляющий шипы в игре.

    Методы:
    - __init__: инициализация объекта шипов.
    """
    def __init__(self, x, y, image_path="objects/torch.png"):
        """
        Инициализация объекта шипов.

        Параметры:
        - x, y: координаты верхнего левого угла шипов.
        - image_path: путь к изображению шипов.
        """
        super().__init__(x, y, image_path="objects/torch.png")
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (32, 16))
        self.image = image.load(image_path)
        self.rect = Rect(x, y, 32, 16)
