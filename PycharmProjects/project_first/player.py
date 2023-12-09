from pygame import *
import pyganim
import enemies

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


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)

        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?

        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

        self.direction = True

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

    def update(self, left, right, up, platforms, attack):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            if self.direction:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
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
            self.image.set_colorkey(Color(COLOR))
            self.image.fill(Color(COLOR))
            if self.direction is True:
                self.boltAnimAttackRight.blit(self.image, (0, 0))
            if self.direction is False:
                self.boltAnimAttackLeft.blit(self.image, (0, 0))

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def die(self):
        time.wait(500)
        self.teleporting(self.startX, self.startY)

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                if isinstance(p, enemies.Enemy):
                    self.die()

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
