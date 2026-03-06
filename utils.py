import pygame

# Configurações da tela (Resolução)
VIRTUAL_WIDTH = 1920
VIRTUAL_HEIGHT = 1080

# Inicialização do Pygame
pygame.init()
info = pygame.display.Info()
MONITOR_WIDTH = info.current_w
MONITOR_HEIGHT = info.current_h

# Configuração Fullscreen
screen = pygame.display.set_mode((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
pygame.display.set_caption("CastleDoom")

# Adição da imagem de fundo
BACKGROUND_IMAGE = pygame.image.load("./assets/Background.png").convert()
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (VIRTUAL_WIDTH, VIRTUAL_HEIGHT))

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