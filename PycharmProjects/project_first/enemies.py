from pygame import *
import pyganim
import time
import math

ANIMATION_MONSTER = [f"assets_sprites/enemy1/enemy{i}.png" for i in range(4)]

ENEMY_COLOR = "#000000"
MONSTER_WIDTH = 24
MONSTER_HEIGHT = 24


class Enemy(sprite.Sprite):
    """
    Класс, представляющий простого врага (Enemy) в игре.

    Attributes:
    - rect: Прямоугольник, определяющий положение врага на экране.
    :type rect: pygame.Rect

    - image: Изображение врага.
    :type image: pygame.Surface

    - startX: Начальная координата по горизонтали.
    :type startX: int

    - startY: Начальная координата по вертикали.
    :type startY: int

    - maxLengthLeft: Максимальное расстояние, которое враг может пройти в одну сторону по горизонтали.
    :type maxLengthLeft: int

    - maxLengthUp: Максимальное расстояние, которое враг может пройти в одну сторону по вертикали.
    :type maxLengthUp: int

    - xvel: Начальная скорость врага по горизонтали.
    :type xvel: int

    - yvel: Начальная скорость врага по вертикали.
    :type yvel: int

    - boltAnim: Анимация врага.
    :type boltAnim: pyganim.PygAnimation

    - hp: Количество очков здоровья врага.
    :type hp: int
    """

    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, hp):
        """
               Инициализирует объект врага.

               :param x: Начальная координата X врага.
               :type x: int
               :param y: Начальная координата Y врага.
               :type y: int
               :param left: Начальная скорость врага по горизонтали.
               :type left: int
               :param up: Начальная скорость врага по вертикали.
               :type up: int
               :param maxLengthLeft: Максимальное расстояние по горизонтали, которое враг может пройти в одну сторону.
               :type maxLengthLeft: int
               :param maxLengthUp: Максимальное расстояние по вертикали, которое враг может пройти в одну сторону.
               :type maxLengthUp: int
               :param hp: Количество очков здоровья врага.
               :type hp: int
               """
        sprite.Sprite.__init__(self)
        self.image = Surface((24, 24))
        self.image.fill(Color(ENEMY_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(ENEMY_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTER:
            boltAnim.append((anim, 90))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

        self.hp = hp

    def update(self, platforms):
        """
               Обновляет положение и состояние врага.

               :param platforms: Список платформ в игре.
               :type platforms: list
               """

        self.image.fill(Color(ENEMY_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = -self.yvel  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        """
        Проверяет столкновение врага с платформами.

        :param platforms: Список платформ в игре.
        :type platforms: list
        """
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel
                self.hp -= 2
                if self.hp <= 0:
                    self.die()

    def die(self):
        """
        Обрабатывает смерть врага.
        """
        if self.hp <= 0:
            self.remove()
            self.kill()


ANIMATION_GOLEM_IDLE = [f'assets_sprites/enemy2/en2_i/en2_idle{i}.png' for i in range(4)]
ANIMATION_GOLEM_WALK_LEFT = [f'assets_sprites/enemy2/en2_w/en2_walk{i}.png' for i in range(7)]
ANIMATION_GOLEM_WALK_RIGHT = [f'assets_sprites/enemy2/en2_w/en2_walk{i}_r.png' for i in range(7)]
ANIMATION_GOLEM_ATTACK_LEFT = [f'assets_sprites/enemy2/en2_a/_en2_attack{i}.png' for i in range(6)]
ANIMATION_GOLEM_ATTACK_RIGHT = [f'assets_sprites/enemy2/en2_a/_en2_attack{i}_r.png' for i in range(5)]
ANIMATION_GOLEM_DIE = [f'assets_sprites/enemy2/en2_d/en2_die{i}.png' for i in range(8)]


class Enemy2(sprite.Sprite):
    """
        Класс, представляющий продвинутого врага (Enemy2) в игре.

        Attributes:
        - image: Изображение врага.
        :type image: pygame.Surface

        - rect: Прямоугольник, определяющий положение врага на экране.
        :type rect: pygame.Rect

        - startX: Начальная координата по горизонтали.
        :type startX: int

        - startY: Начальная координата по вертикали.
        :type startY: int

        - maxLengthLeft: Максимальное расстояние по горизонтали, которое враг может пройти в одну сторону.
        :type maxLengthLeft: int

        - maxLengthUp: Максимальное расстояние по вертикали, которое враг может пройти в одну сторону.
        :type maxLengthUp: int

        - xvel: Начальная скорость врага по горизонтали.
        :type xvel: int

        - yvel: Начальная скорость врага по вертикали.
        :type yvel: int

        - direction: Направление врага (True - вправо, False - влево).
        :type direction: bool

        - hp: Количество очков здоровья врага.
        :type hp: int

        - start_time: Время начала движения врага.
        :type start_time: float

        - elapsed_time: Прошедшее время.
        :type elapsed_time: float

        - paused: Флаг паузы.
        :type paused: bool

        - player: Объект игрока.
        :type player: Player

        - attack_range: Радиус, в пределах которого враг начинает атаковать.
        :type attack_range: int

        - attack_distance: Дистанция атаки.
        :type attack_distance: int

        - boltAnimDie: Анимация смерти врага.
        :type boltAnimDie: pyganim.PygAnimation

        - boltAnimIdle: Анимация покоя врага.
        :type boltAnimIdle: pyganim.PygAnimation

        - boltAnimWalkLeft: Анимация движения влево.
        :type boltAnimWalkLeft: pyganim.PygAnimation

        - boltAnimWalkRight: Анимация движения вправо.
        :type boltAnimWalkRight: pyganim.PygAnimation

        - boltAnimAttackLeft: Анимация атаки влево.
        :type boltAnimAttackLeft: pyganim.PygAnimation

        - boltAnimAttackRight: Анимация атаки вправо.
        :type boltAnimAttackRight: pyganim.PygAnimation
        """

    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, player, hp):
        """
              Инициализирует объект продвинутого врага.

              :param x: Начальная координата X врага.
              :type x: int
              :param y: Начальная координата Y врага.
              :type y: int
              :param left: Начальная скорость врага по горизонтали.
              :type left: int
              :param up: Начальная скорость врага по вертикали.
              :type up: int
              :param maxLengthLeft: Максимальное расстояние по горизонтали, которое враг может пройти в одну сторону.
              :type maxLengthLeft: int
              :param maxLengthUp: Максимальное расстояние по вертикали, которое враг может пройти в одну сторону.
              :type maxLengthUp: int
              :param player: Объект игрока.
              :type player: Player
              :param hp: Количество очков здоровья врага.
              :type hp: int
              """

        sprite.Sprite.__init__(self)
        self.image = Surface((96, 96))
        self.image.fill(Color(ENEMY_COLOR))
        self.rect = Rect(x, y, 96, 96)
        self.image.set_colorkey(Color(ENEMY_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxLengthLeft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxLengthUp  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается

        self.direction = True  # left

        self.hp = hp

        self.start_time = time.time()
        self.elapsed_time = 0
        self.paused = False

        self.player = player
        self.attack_range = 200
        self.attack_distance = 10

        boltAnim = []
        for anim in ANIMATION_GOLEM_DIE:
            boltAnim.append((anim, 120))
        self.boltAnimDie = pyganim.PygAnimation(boltAnim)
        self.boltAnimDie.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_IDLE:
            boltAnim.append((anim, 120))
        self.boltAnimIdle = pyganim.PygAnimation(boltAnim)
        self.boltAnimIdle.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_WALK_LEFT:
            boltAnim.append((anim, 120))
        self.boltAnimWalkLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalkLeft.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_WALK_RIGHT:
            boltAnim.append((anim, 120))
        self.boltAnimWalkRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalkRight.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_DIE:
            boltAnim.append((anim, 120))
        self.boltAnimDie = pyganim.PygAnimation(boltAnim)
        self.boltAnimDie.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_ATTACK_RIGHT:
            boltAnim.append((anim, 120))
        self.boltAnimAttackRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttackRight.play()

        boltAnim = []
        for anim in ANIMATION_GOLEM_ATTACK_LEFT:
            boltAnim.append((anim, 120))
        self.boltAnimAttackLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttackLeft.play()

    def collide(self, platforms):
        """
               Обрабатывает столкновения врага с платформами.

               :param platforms: Список платформ, с которыми может столкнуться враг.
               :type platforms: list[Platform]
               """
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel
                self.hp -= 2
                if self.hp <= 0:
                    self.die(platforms)

    def die(self, platforms):
        """
              Обрабатывает смерть врага.

              :param platforms: Список платформ, с которыми может столкнуться враг.
              :type platforms: list[Platform]
              """
        self.kill()
        platforms.remove(self)

    def update(self, platforms):
        """
              Обновляет состояние врага.

              :param platforms: Список платформ, с которыми может столкнуться враг.
              :type platforms: list[Platform]
              """

        player_distance = math.sqrt((self.rect.x - self.player.rect.x) ** 2 + (self.rect.y - self.player.rect.y) ** 2)

        # Приблизительное расстояние, на котором Enemy2 начнет атаковать
        attack_range = 128

        if player_distance < attack_range:
            self.xvel = 0  # Останавливаем Enemy2
            self.attack_animation()
        else:
            if self.direction:
                self.xvel = 1
                self.image.fill(Color(ENEMY_COLOR))
                self.boltAnimWalkRight.blit(self.image, (0, 0))
            else:
                self.xvel = -1
                self.image.fill(Color(ENEMY_COLOR))
                self.boltAnimWalkLeft.blit(self.image, (0, 0))
            self.rect.x += self.xvel

            if abs(self.startX - self.rect.x) > self.maxLengthLeft:
                self.direction = not self.direction

    def attack_animation(self):
        """Анимация атаки врага."""
        self.image.fill(Color(ENEMY_COLOR))
        if self.player.direction:
            self.boltAnimAttackLeft.blit(self.image, (0, 0))
        else:
            self.boltAnimAttackRight.blit(self.image, (0, 0))
