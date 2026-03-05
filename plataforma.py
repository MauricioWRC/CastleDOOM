import pygame
import utils as u

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(u.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y