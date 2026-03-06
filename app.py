import pygame
import sys
import random

import utils as u
from build import Plataforma, Player, Inimigo, InimigoVoador

# Grupos de sprites
sprites = pygame.sprite.Group()
platformas = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
voadores = pygame.sprite.Group()

# Plataformas
lista_plataformas = [
    # (x, y, Largura, Altura)
    (0, 1000, 1920, 80),    # CHÃO: Preenche toda a base
    (860, 750, 200, 20),    # Plataforma central inferior
    (300, 550, 300, 20),    # Plataforma média esquerda
    (1300, 500, 350, 20),   # Plataforma média direita
    (0, 180, 250, 20),      # Plataforma superior esquerda
    (1600, 160, 320, 20)    # Plataforma superior direita
]

for plat in lista_plataformas:
    p = Plataforma(*plat)
    sprites.add(p)
    platformas.add(p)
    
# Jogador
player = Player()
sprites.add(player)

# Inimigos
spawn_types = ["chao_esquerda", "chao_direita", "ceu_esquerda", "ceu_direita"]
for _ in range(5):
    spawn_type = random.choice(spawn_types)
    enemy = Inimigo(spawn_type)
    sprites.add(enemy)
    inimigos.add(enemy)

# Spawn inicial de voadores
for _ in range(2):
    v = InimigoVoador()
    sprites.add(v)
    voadores.add(v)

# Loop principal
def main():
    
    rodando = True
    
    # Timer para spawnar inimigos a cada 5 segundos
    tempo_spawn = 4000  # 4 segundos
    ultimo_spawn = pygame.time.get_ticks()
    
    while rodando:
        
        agora = pygame.time.get_ticks()
        
        # 1.Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: # Permite sair do jogo com a tecla ESC
                    rodando = False
                if evento.key == pygame.K_SPACE:
                    player.jump(platformas)
                    
        # Eventos de inimigos
        if agora - ultimo_spawn > tempo_spawn:
            for _ in range(3):
                tipo_spawn = random.choice(spawn_types)
                inimigo = Inimigo(tipo_spawn)
                sprites.add(inimigo)
                inimigos.add(inimigo)
            ultimo_spawn = agora

        # Respawn de voadores: só quando zerar o grupo
        if len(voadores) == 0:
            qtd = random.randint(1, 3)
            for _ in range(qtd):
                v = InimigoVoador()
                sprites.add(v)
                voadores.add(v)
            
        # 2.Atualização
        player.update(platformas)
        
        for inimigo in inimigos:
            inimigo.update(platformas, player)

        # Atualiza voadores
        voadores.update()

        # Atualizar plataformas
        platformas.update(platformas)
        
        # Colisão entre jogador e inimigos
        hit_inimigo = pygame.sprite.spritecollide(player, inimigos, True)
        hit_voador = pygame.sprite.spritecollide(player, voadores, True)
        
        # 3.Desenho
        u.screen.fill(u.WHITE)
        sprites.draw(u.screen)
        
        pygame.display.flip()
        u.clock.tick(u.FPS)
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()