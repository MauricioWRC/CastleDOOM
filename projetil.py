import pygame
import math
import utils as u
import random
import os

# Função auxiliar para carregar imagens com segurança
def carregar_imagem_projetil(nome_arquivo):
    # Tenta carregar a imagem da pasta 'assets' ou da pasta raiz
    caminho_assets = os.path.join('assets', nome_arquivo)
    
    if os.path.exists(caminho_assets):
        # Carrega e converte para performance mantendo transparência
        return pygame.image.load(caminho_assets).convert_alpha()
    elif os.path.exists(nome_arquivo):
        return pygame.image.load(nome_arquivo).convert_alpha()
    else:
        # Se a imagem não for encontrada, cria um retângulo colorido de fallback
        # para o jogo não quebrar, mas avisa no console.
        print(f"AVISO: Imagem {nome_arquivo} não encontrada. Usando fallback.")
        fallback = pygame.Surface((40, 40))
        fallback.fill((255, 0, 255)) # Magenta choque para destacar o erro
        return fallback

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        
        # --- NOVO: Carregando a Splash Art ---
        # Carrega a imagem especificada
        self.image = carregar_imagem_projetil('img/ProjetilPlayer.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        
        # Opcional: Se a imagem for muito grande/pequena, você pode redimensionar aqui
        # self.image = pygame.transform.scale(self.image, (25, 25))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 22 
        
        # Lógica de direção permanece a mesma
        dx = target_x - x
        dy = target_y - y
        angle = math.atan2(dy, dx)
        angle_deg = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle_deg)
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > u.VIRTUAL_WIDTH or
            self.rect.bottom < 0 or self.rect.top > u.VIRTUAL_HEIGHT):
            self.kill()

class ProjetilInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        
        # --- NOVO: Carregando a Splash Art ---
        self.image = carregar_imagem_projetil('img/ProjetilInimigo.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10
        
        # Erro de mira
        desvio_x = random.randint(-100, 100)
        desvio_y = random.randint(-100, 100)
        
        dx = (target_x + desvio_x) - x
        dy = (target_y + desvio_y) - y
        angle = math.atan2(dy, dx)
        angle_deg = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.image, angle_deg)
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > u.VIRTUAL_WIDTH or
            self.rect.bottom < 0 or self.rect.top > u.VIRTUAL_HEIGHT):
            self.kill()