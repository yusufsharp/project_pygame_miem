import pygame
import sys
from utils.settings import *
from pygame.locals import *
from objects.player import Player

pygame.init()

BACKGROUND = (0, 0, 0)
vec = pygame.math.Vector2  # creating vector object

# pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()





# classes
# ground = Ground()
# ground_group = pygame.sprite.Group()
# ground_group.add(ground)
player = Player()

while True:
    player.gravity_check()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    screen.fill(BACKGROUND)

    # render func
    player.update()
    player.move()
    screen.blit(player.image, player.rect)

    pygame.display.update()
    FPS_CLOCK.tick(FPS)
