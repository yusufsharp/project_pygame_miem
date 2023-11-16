import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image_path, start_x, start_y):
        super().__init__()

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        self.rect.center = [start_x, start_y]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)