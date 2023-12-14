from pygame import *
import pyganim

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
