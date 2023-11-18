import pygame


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("media/images/Ground.png")
        self.rect = pygame.image.get_rect(center=(350, 350))
