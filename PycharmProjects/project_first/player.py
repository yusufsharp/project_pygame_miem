import sys
from pygame import *
from blocks import Platform, MovingPlatform, Lava, Teleport, Thorns
from enemies import *
from settings import *
import pygame
from menu import death_screen

MOVE_SPEED = 7
ATTACK_WIDTH = 84
ATTACK_HEIGHT = 84
WIDTH = 64
HEIGHT = 64
COLOR = "#000000"
JUMP_POWER = 13
GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

ANIMATION_DELAY = 60
ANIMATION_RIGHT = [f"assets_sprites/Run/run_r{i}.png" for i in range(1, 9)]
ANIMATION_LEFT = [f"assets_sprites/Run/run_l{i}.png" for i in range(1, 9)]
ANIMATION_JUMP_RIGHT = [f'assets_sprites/Jump-All/jump_r{i}.png' for i in range(1, 9)]
ANIMATION_JUMP_LEFT = [f'assets_sprites/Jump-All/jump_l{i}.png' for i in range(1, 9)]
ANIMATION_STAY_LEFT = [f"assets_sprites/idle/Idle_l{i}.png" for i in range(4)]
ANIMATION_STAY_RIGHT = [f"assets_sprites/idle/Idle_r{i}.png" for i in range(5)]
ANIMATION_ATTACK_RIGHT = [f'assets_sprites/Attack-01/attack_r{i}.png' for i in range(1, 6)]
ANIMATION_ATTACK_LEFT = [f'assets_sprites/Attack-01/attack_l{i}.png' for i in range(1, 6)]

pygame.init()

enemy = Enemy
golem = Enemy2

color_light = (170, 170, 170)
color_dark = (100, 100, 100)
color_white = (255, 255, 255)


class HealthBar():
    """
    Класс HealthBar представляет полосу здоровья для отображения состояния здоровья игрока.

    Attributes:
    - x: координата X верхнего левого угла полосы здоровья.
    - y: координата Y верхнего левого угла полосы здоровья.
    - w: ширина полосы здоровья.
    - h: высота полосы здоровья.
    - hp: текущее количество здоровья игрока.
    - max_hp: максимальное количество здоровья игрока.

    Methods:
    - __init__(self, x, y, w, h, max_hp): конструктор класса.
    - draw(self, surface): отрисовка полосы здоровья на экране.
    """
    def __init__(self, x, y, w, h, max_hp):
        """
          Класс HealthBar для отображения здоровья игрока.

          :param x: Координата X верхнего левого угла полосы здоровья.
          :param y: Координата Y верхнего левого угла полосы здоровья.
          :param w: Ширина полосы здоровья.
          :param h: Высота полосы здоровья.
          :param max_hp: Максимальное количество здоровья игрока.
          :type x: int
          :type y: int
          :type w: int
          :type h: int
          :type max_hp: int
          """
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        """
            Отрисовка полосы здоровья на экране.

            :param surface: Поверхность, на которой отрисовывается полоса здоровья.
            :type surface: pygame.Surface
            """
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h), border_radius=20)
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h), border_radius=20)


class Player(sprite.Sprite):
    """
    Класс Player представляет игрового персонажа.

    Attributes:
    - xvel: скорость перемещения по горизонтали.
    - startX: начальная позиция по горизонтали.
    - startY: начальная позиция по вертикали.
    - yvel: скорость перемещения по вертикали.
    - onGround: флаг, указывающий, находится ли персонаж на земле.
    - next_level: флаг, указывающий, что персонаж перешел на следующий уровень.
    - restart: флаг, указывающий, что нужно перезапустить игру.
    - image: изображение персонажа.
    - rect: прямоугольник, описывающий положение и размер персонажа на экране.
    - direction: направление персонажа (True - вправо, False - влево).
    - on_moving_platform: флаг, указывающий, находится ли персонаж на подвижной платформе.
    - exp: опыт игрока.
    - time: время, проведенное в игре в формате 'минуты:секунды'.
    - health_bar: полоса здоровья персонажа.

    Methods:
    - __init__(self, x, y, screen, username, exp): конструктор класса.
    - draw_health_bar(self, surface): отрисовка полосы здоровья на указанной поверхности.
    - update(self, left, right, up, platforms, attack, screen, username): обновление состояния персонажа.
    - die(self, screen): обработка смерти персонажа.
    - recive_attack(self, damage): обработка получения урона персонажем.
    - collide(self, xvel, yvel, platforms, attack, screen): обработка столкновений с платформами и объектами.
    """
    def __init__(self, x, y, screen, username, exp):
        sprite.Sprite.__init__(self)

        """
           Конструктор класса Player для отображения игрока.

           Параметры:
           - x, y: начальные координаты игрока.
           - screen: поверхность, на которой отображается игра.
           - username: имя игрока.
           - exp: опыт игрока.
           """

        self.username = username

        self.screen = screen

        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.next_level = False
        self.restart = False

        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

        self.direction = True
        self.on_moving_platform = False

        self.exp = exp
        total_seconds = pygame.time.get_ticks() // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.time = f'{minutes}:{seconds}'

        self.health_bar = HealthBar(164, 50, 128, 24, max_hp=100)

        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        boltAnim = []
        for anim in ANIMATION_STAY_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimStayRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimStayRight.play()

        boltAnim = []
        for anim in ANIMATION_STAY_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimStayLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimStayLeft.play()

        if self.direction:
            self.boltAnimStayRight.blit(self.image, (0, 0))  # По-умолчанию, стоим
        else:
            self.boltAnimStayLeft.blit(self.image, (0, 0))

        boltAnim = []
        for anim in ANIMATION_JUMP_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJumpRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpRight.play()

        boltAnim = []
        for anim in ANIMATION_JUMP_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJumpLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimJumpLeft.play()

        boltAnim = []
        for anim in ANIMATION_ATTACK_RIGHT:
            boltAnim.append((anim, 60))
        self.boltAnimAttackRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttackRight.play()

        boltAnim = []
        for anim in ANIMATION_ATTACK_LEFT:
            boltAnim.append((anim, 60))
        self.boltAnimAttackLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttackLeft.play()

    def draw_health_bar(self, surface):
        """
        Отрисовка шкалы здоровья.

        :param surface: поверхность, на которой отображается шкала.
        """
        self.health_bar.draw(surface)

    def update(self, left, right, up, platforms, attack, screen, username):
        """
        Обновляет состояние игрока в соответствии с переданными параметрами.

        :param left: Флаг направления движения влево.
        :type left: bool
        :param right: Флаг направления движения вправо.
        :type right: bool
        :param up: Флаг прыжка.
        :type up: bool
        :param platforms: Список платформ в уровне.
        :type platforms: list
        :param attack: Флаг атаки игрока.
        :type attack: bool
        :param screen: Поверхность, на которой отображается игра.
        :type screen: pygame.Surface
        :param username: Имя игрока.
        :type username: str
        """
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            if self.direction:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))

            self.on_moving_platform = False
        if left:
            self.direction = False
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:

            self.direction = True
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                if self.direction:
                    self.boltAnimStayRight.blit(self.image, (0, 0))
                else:
                    self.boltAnimStayLeft.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY

        if attack:
            self.image = Surface((ATTACK_WIDTH, ATTACK_HEIGHT))
            self.image.fill(Color(COLOR))
            self.image.set_colorkey(Color(COLOR))
            if self.direction is True:
                self.boltAnimAttackRight.blit(self.image, (0, 0))
            if self.direction is False:
                self.boltAnimAttackLeft.blit(self.image, (0, 0))

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, attack, screen)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, attack, screen)

    def die(self, screen):
        """
            Обрабатывает смерть персонажа и вызывает соответствующий экран смерти.

            :param screen: Поверхность, на которой отображается игра.
            """
        self.restart = death_screen(screen)

    def collide(self, xvel, yvel, platforms, attack, screen):
        """
           Обрабатывает столкновения игрока с платформами и врагами.

           :param xvel: Скорость по горизонтали.
           :type xvel: float
           :param yvel: Скорость по вертикали.
           :type yvel: float
           :param platforms: Список платформ в уровне.
           :type platforms: list
           :param attack: Флаг атаки игрока.
           :type attack: bool
           :param screen: Поверхность, на которой отображается игра.
           """
        for p in platforms:
            if sprite.collide_rect(self, p) and not isinstance(p,
                                                               Teleport):  # если есть пересечение платформы с игроком
                if isinstance(p, Enemy):
                    if attack:
                        p.hp -= 3
                    else:
                        damage = 0.5
                        self.health_bar.hp -= damage
                        if self.health_bar.hp <= 0:
                            self.die(screen)
                if isinstance(p, Enemy2):
                    if attack:
                        p.hp -= 3
                    damage = 1
                    self.health_bar.hp -= damage
                    if self.health_bar.hp <= 0:
                        self.die(screen)

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает

                if isinstance(p, MovingPlatform):
                    self.on_moving_platform = True
                else:
                    self.on_moving_platform = False
                if isinstance(p, Lava):
                    self.die(screen)
                if isinstance(p, Thorns):
                    self.health_bar.hp -= 10
                    if self.health_bar.hp <= 0:
                        self.die(screen)

            if sprite.collide_rect(self, p) and isinstance(p, Teleport):
                self.next_level = True


class AttackEffect(sprite.Sprite):
    """
        Класс AttackEffect представляет эффект атаки игрока.

        Atributes:
        - player: объект игрока, относительно которого отображается эффект
        - image: изображение эффекта
        - rect: прямоугольник, описывающий положение и размер эффекта на экране
        - boltAnimAttack: анимация эффекта атаки

        Metods:
        - __init__(self, player): конструктор класса
        - update(self, attack, platforms, hero): обновление состояния эффекта атаки
        - collide(self, platforms, attack, hero): обработка столкновений эффекта атаки с объектами
        - draw(self, attack, surface): отрисовка эффекта атаки на поверхности
        """

    def __init__(self, player):
        super().__init__()
        """
                Инициализация экземпляра класса AttackEffect.

                :param player: объект игрока, относительно которого отображается эффект
                :type player: Player
                """
        self.player = player
        self.image = Surface((ATTACK_WIDTH, ATTACK_HEIGHT))
        self.image.set_colorkey(Color(COLOR))
        self.rect = self.image.get_rect()

        ANIMATION_ATTACK = [f"assets_sprites/attack/NPT10{i}.png" for i in range(4)]

        boltAnim = []
        for anim in ANIMATION_ATTACK:
            boltAnim.append((anim, 60))
        self.boltAnimAttack = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttack.play()

        # Установите начальные координаты эффекта атаки относительно игрока
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

    def update(self, attack, platforms, hero):
        """
                Обновление состояния эффекта атаки.

                :param attack: флаг атаки
                :type attack: bool
                :param platforms: список платформ в уровне
                :type platforms: List[Platform]
                :param hero: объект игрока
                :type hero: Player
                :returns: None
                """
        if attack:
            if self.player.direction:
                self.rect.centerx = self.player.rect.centerx + 64
                self.rect.centery = self.player.rect.centery
            else:
                self.rect.centerx = self.player.rect.centerx - 64
                self.rect.centery = self.player.rect.centery
            self.image.fill(Color(COLOR))
            self.boltAnimAttack.blit(self.image, (0, 0))
        else:
            self.rect.centerx = -10000
            self.rect.centery = -10000

        self.collide(platforms, attack, hero)

    def collide(self, platforms, attack, hero):
        """
            Обработка столкновений эффекта атаки с объектами.

            :param platforms: список платформ в уровне
            :type platforms: List[Platform]
            :param attack: флаг атаки
            :type attack: bool
            :param hero: объект игрока
            :type hero: Player
            :returns: None
            """
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, Enemy):
                    if attack:
                        p.hp -= 2
                        if p.hp <= 0:
                            platforms.remove(p)
                            p.kill()
                            hero.exp += 10
                    else:
                        damage = 2
                        self.health_bar.hp -= damage
                        if self.health_bar.hp <= 0:
                            self.die()
                if isinstance(p, Enemy2):
                    if attack:
                        p.hp -= 2
                        if p.hp <= 0:
                            p.die(platforms)
                            hero.exp += 20

    def draw(self, attack, surface):
        """
               Отрисовка эффекта атаки на указанной поверхности.

               :param attack: флаг атаки
               :type attack: bool
               :param surface: поверхность для отрисовки
               :returns: None
               """
        if attack:
            surface.blit(self.image, self.rect.topleft)


class StatusBar(sprite.Sprite):
    """
    Класс StatusBar представляет статус-панель игрока.

    Atributes:
    - x: координата X верхнего левого угла панели
    - y: координата Y верхнего левого угла панели
    - screen: объект экрана Pygame
    - font: шрифт для отображения текста на панели
    - image: изображение панели с прозрачным фоном
    - rect: прямоугольник, описывающий положение и размер панели на экране

    Metods:
    - __init__(self, x, y, screen): конструктор класса
    - update(self, player, time): обновление содержимого панели
    """
    def __init__(self, x, y, screen):
        """
        Инициализация экземпляра класса StatusBar.

        :param x: координата X верхнего левого угла панели
        :type x: int
        :param y: координата Y верхнего левого угла панели
        :type y: int
        :param screen: объект экрана Pygame
        :type screen: pygame.Surface
        """
        sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont('Corbel', 25)
        self.image = Surface((200, 200), pygame.SRCALPHA)
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, 320, 130)
        self.screen = screen

    def update(self, player, time):
        """
               Обновление содержимого статус-панели.

               :param player: объект игрока
               :type player: Player
               :param time: текущее время игры
               :type time: int
               :returns: None
               """
        username_text = self.font.render(f"USERNAME: {player.username}", True, (255, 255, 255))
        exp_text = self.font.render(f"EXP: {player.exp}", True, (255, 255, 255))
        total_seconds = time // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_text = self.font.render(f"TIME: {minutes:02}:{seconds:02}", True, (255, 255, 255))
        fps_text = self.font.render(f"FPS: {int(FPS_CLOCK.get_fps())}", True, (255, 255, 255))

        # Draw the text on the status bar
        pygame.draw.rect(self.screen, (51, 0, 51), self.rect)
        self.screen.blit(username_text, (self.rect.x + 10, self.rect.y + 10))
        self.screen.blit(exp_text, (self.rect.x + 10, self.rect.y + 40))
        self.screen.blit(time_text, (self.rect.x + 10, self.rect.y + 70))
        self.screen.blit(fps_text, (self.rect.x + 10, self.rect.y + 100))

