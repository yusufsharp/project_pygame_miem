from pygame import *
import pyganim
import time
import math

ANIMATION_MONSTER = [f"assets_sprites/enemy1/enemy{i}.png" for i in range(4)]

ENEMY_COLOR = "#000000"
MONSTER_WIDTH = 24
MONSTER_HEIGHT = 24


class Enemy(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
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

    def update(self, platforms):

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
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel

    def die(self):
        self.kill()


ANIMATION_GOLEM_IDLE = [f'assets_sprites/enemy2/en2_i/en2_idle{i}.png' for i in range(4)]
ANIMATION_GOLEM_WALK_LEFT = [f'assets_sprites/enemy2/en2_w/en2_walk{i}.png' for i in range(7)]
ANIMATION_GOLEM_WALK_RIGHT = [f'assets_sprites/enemy2/en2_w/en2_walk{i}_r.png' for i in range(7)]
ANIMATION_GOLEM_ATTACK_LEFT = [f'assets_sprites/enemy2/en2_a/en2_attack{i}.png' for i in range(6)]
ANIMATION_GOLEM_ATTACK_RIGHT = [f'assets_sprites/enemy2/en2_a/en2_attack{i}_r.png' for i in range(5)]
ANIMATION_GOLEM_DIE = [f'assets_sprites/enemy2/en2_d/en2_die{i}.png' for i in range(8)]


class Enemy2(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp, player):
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

        self.start_time = time.time()
        self.elapsed_time = 0
        self.paused = False

        self.player = player
        self.attack_range = 200
        self.attack_distance = 10

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
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p:
                self.xvel = - self.xvel
                self.yvel = - self.yvel

    def attack(self):
        print('enemy is attacking')
        if self.direction_to_player == 1:
            self.image.fill(Color(ENEMY_COLOR))
            self.boltAnimAttackRight.blit(self.image, (0, 0))
        else:
            self.image.fill(Color(ENEMY_COLOR))
            self.boltAnimAttackLeft.blit(self.image, (0, 0))

    def update(self, platforms):
        distance_to_player = math.sqrt((self.rect.x - self.player.rect.x)**2 + (self.rect.y - self.player.rect.y)**2)

        if distance_to_player < self.attack_distance:
            self.attack()
        if distance_to_player < self.attack_range:
            if self.player.rect.x > self.rect.x:
                self.direction_to_player = 1
            else:
                self.direction_to_player = -1

            self.xvel = self.direction_to_player * 3

            self.direction = self.direction_to_player == 1

        else:
            self.update_passive(platforms)

    def update_passive(self, platforms):
        self.rect.x += self.xvel

        self.collide(platforms)

        if self.xvel > 0:
            self.direction = True
            self.image.fill(Color(ENEMY_COLOR))
            self.boltAnimWalkRight.blit(self.image, (0, 0))
        elif self.xvel < 0:
            self.direction = False
            self.image.fill(Color(ENEMY_COLOR))
            self.boltAnimWalkLeft.blit(self.image, (0, 0))
        else:
            self.image.fill(Color(ENEMY_COLOR))
            self.boltAnimIdle.blit(self.image, (0, 0))

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = -self.xvel

