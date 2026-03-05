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

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Relógio para controlar o FPS
clock = pygame.time.Clock()
FPS = 60