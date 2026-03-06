import pygame
import os

# Configurações da tela (Resolução)
VIRTUAL_WIDTH = 1920
VIRTUAL_HEIGHT = 1080

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

# Configuração Fullscreen
screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("CastleDoom")
pygame.display.set_caption("CastleDoom")

# --- Música de fundo ---
pygame.mixer.music.load("assets/musica.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  # loop infinito
# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# Fonte para o contador
pygame.font.init()
FONTE_HUD = pygame.font.SysFont("Arial", 40, bold=True)

clock = pygame.time.Clock()
FPS = 60

# --- NOVO: Sistema de Imagens Inteligente ---
def carregar_imagem(caminho, tamanho, cor_padrao):
    """
    Tenta carregar uma imagem da pasta. 
    Se o ficheiro não existir, cria um quadrado com a cor padrão.
    """
    if os.path.exists(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    else:
        surf = pygame.Surface(tamanho, pygame.SRCALPHA)
        surf.fill(cor_padrao)
        return surf

# Carrega o fundo (se não achar, fica branco)
IMG_FUNDO = carregar_imagem("assets/Background.png", (VIRTUAL_WIDTH, VIRTUAL_HEIGHT), WHITE)