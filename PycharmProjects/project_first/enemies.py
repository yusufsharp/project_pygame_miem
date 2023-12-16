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

    Параметры:
    - x, y: начальные координаты врага.
    - left, up: начальная скорость врага по горизонтали и вертикали.
    - maxLengthLeft: максимальное расстояние, которое враг может пройти в одну сторону по горизонтали.
    - maxLengthUp: максимальное расстояние, которое враг может пройти в одну сторону по вертикали.
    - hp: количество очков здоровья врага.
    """
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, hp):
        """
        Инициализирует объект врага.

        Параметры:
        - x, y: начальные координаты врага.
        - left, up: начальная скорость врага по горизонтали и вертикали.
        - maxLengthLeft: максимальное расстояние, которое враг может пройти в одну сторону по горизонтали.
        - maxLengthUp: максимальное расстояние, которое враг может пройти в одну сторону по вертикали.
        - hp: количество очков здоровья врага.
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

            Параметры:
            - platforms: список платформ в игре.
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

            Параметры:
            - platforms: список платформ в игре.
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
    Класс, представляющий второго врага в игре.

    Атрибуты:
    - image: изображение врага.
    - rect: прямоугольник, определяющий положение и размеры врага.
    - startX, startY: начальные координаты врага.
    - maxLengthLeft: максимальное расстояние, которое враг может пройти в одну сторону по горизонтали.
    - maxLengthUp: максимальное расстояние, которое враг может пройти в одну сторону по вертикали.
    - xvel, yvel: скорость движения врага по горизонтали и вертикали.
    - direction: направление движения врага (True - влево, False - вправо).
    - hp: количество очков здоровья врага.
    - start_time: время начала существования врага.
    - elapsed_time: прошедшее время с начала существования врага.
    - paused: флаг паузы (True - враг приостановлен).
    - player: объект игрока, за которым будет охотиться враг.
    - attack_range: расстояние, на котором враг начнет атаковать игрока.
    - attack_distance: дистанция атаки врага.

    Методы:
    - __init__: инициализация объекта врага.
    - collide: обработка столкновений врага с платформами.
    - die: обработка смерти врага.
    - update: обновление состояния врага.
    - attack_animation: анимация атаки врага.
    """
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, player, hp):
        """
         Инициализирует объект второго врага.

         Параметры:
         - x, y: начальные координаты врага.
         - left, up: начальная скорость врага по горизонтали и вертикали.
         - maxLengthLeft: максимальное расстояние, которое враг может пройти в одну сторону по горизонтали.
         - maxLengthUp: максимальное расстояние, которое враг может пройти в одну сторону по вертикали.
         - player: объект игрока, за которым будет охотиться враг.
         - hp: количество очков здоровья врага.
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
        Обработка столкновений врага с платформами.

        Параметры:
        - platforms: список платформ, с которыми может столкнуться враг.
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
        Обработка смерти врага.

        Параметры:
        - platforms: список платформ, с которыми может столкнуться враг.
        """
        self.kill()
        platforms.remove(self)

    def update(self, platforms):
        """
         Обновление состояния врага.

         Параметры:
         - platforms: список платформ, с которыми может столкнуться враг.
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
