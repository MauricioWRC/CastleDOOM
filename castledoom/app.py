import pygame
from pygame.locals import *
from sys import exit
import random
import math


pygame.init()

info = pygame.display.Info()
TELA_LARGURA = info.current_w
TELA_ALTURA = info.current_h
FPS = 60


tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Invaders")
relogio = pygame.time.Clock()
