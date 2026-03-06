import pygame
import math
import utils as u
import random

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()

        self.image = pygame.image.load("./assets/ProjetilPlayer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        #self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        #pygame.draw.circle(self.image, u.YELLOW, (12, 12), 12)
        
        dx = target_x - x
        dy = target_y - y
        angle = math.atan2(dy, dx)

        self.speed = 22 
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed

        angle_deg = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle_deg)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > u.VIRTUAL_WIDTH or
            self.rect.bottom < 0 or self.rect.top > u.VIRTUAL_HEIGHT):
            self.kill()

class ProjetilInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()

        self.image = pygame.image.load("./assets/ProjetilInimigo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        #self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        #pygame.draw.circle(self.image, (255, 100, 0), (10, 10), 10) # Laranja/Vermelho
       
        # Erro de mira: adiciona um desvio aleatório entre -100 e 100 pixels
        desvio_x = random.randint(-100, 100)
        desvio_y = random.randint(-100, 100)
        
        dx = (target_x + desvio_x) - x
        dy = (target_y + desvio_y) - y
        angle = math.atan2(dy, dx)
 
        self.speed = 10 # Mais lento que o do player
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed

        angle_deg = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle_deg)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > u.VIRTUAL_WIDTH or
            self.rect.bottom < 0 or self.rect.top > u.VIRTUAL_HEIGHT):
            self.kill()