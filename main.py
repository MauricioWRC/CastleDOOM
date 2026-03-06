import pygame
import sys
import random
import utils as u
from plataforma import Plataforma
from player import Player
from inimigos import Inimigo, InimigoVoador, InimigoEstatico
from projetil import ProjetilInimigo

# Grupos
sprites = pygame.sprite.Group()
platformas = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
voadores = pygame.sprite.Group()
projeteis_player = pygame.sprite.Group()
projeteis_inimigos = pygame.sprite.Group()

abates = 0
fila_respawn_topo = []

# Configuração de plataformas
lista_plataformas = [(0, 1000, 1920, 80), (860, 750, 200, 20), (300, 550, 300, 20), (1300, 500, 350, 20), (0, 180, 250, 20), (1600, 160, 320, 20)]
for plat in lista_plataformas:
    p = Plataforma(*plat)
    sprites.add(p); platformas.add(p)

player = Player()
sprites.add(player)

# Guardas iniciais
for pos in ["topo_esquerda", "topo_direita"]:
    g = InimigoEstatico(pos)
    sprites.add(g); inimigos.add(g)

def main():
    global abates
    rodando = True
    ultimo_spawn_chao = pygame.time.get_ticks()
    ultimo_spawn_voador = pygame.time.get_ticks() 
    
    while rodando:
        agora = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE: 
                    rodando = False
                if evento.key == pygame.K_SPACE or evento.key == pygame.K_w: 
                    player.jump(platformas)

        # Controles do Rato (Mouse)
        botoes_rato = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos() # Pegamos a posição do rato uma vez aqui
        
        # Botão Esquerdo [0] - Atirar
        if botoes_rato[0]:
            player.atirar(mx, my, sprites, projeteis_player)
            
        # Botão Direito [2] - Ataque Corpo a Corpo Contínuo!
        if botoes_rato[2]:
            novos_abates = player.atacar_melee_continuo(mx, my, sprites, inimigos, voadores)
            abates += novos_abates
        else:
            # Se não estiver a segurar o botão, a aura desaparece
            player.parar_melee()
                    
        # Lógica de Respawn (Topo)
        for item in fila_respawn_topo[:]:
            if agora >= item[0]:
                novo = InimigoEstatico(item[1])
                sprites.add(novo); inimigos.add(novo)
                fila_respawn_topo.remove(item)

        # SPAWN: Inimigos do chão 
        if agora - ultimo_spawn_chao > 2000:
            e = Inimigo(random.choice(["chao_esquerda", "chao_direita"]))
            sprites.add(e); inimigos.add(e)
            ultimo_spawn_chao = agora
            
        # SPAWN: Inimigos Voadores 
        if agora - ultimo_spawn_voador > 4500:
            v = InimigoVoador()
            sprites.add(v); voadores.add(v)
            ultimo_spawn_voador = agora

        # --- Atualizações ---
        player.update(platformas)
        
        for inimigo in inimigos:
            acao = inimigo.update(platformas, player)
            if acao == "atirar":
                tiro_i = ProjetilInimigo(inimigo.rect.centerx, inimigo.rect.centery, player.rect.centerx, player.rect.centery)
                sprites.add(tiro_i); projeteis_inimigos.add(tiro_i)
        
        voadores.update()
        projeteis_player.update()
        projeteis_inimigos.update()

        # --- Colisões ---
        # 1. Player toma dano por projéteis
        if pygame.sprite.spritecollide(player, projeteis_inimigos, True):
            player.tomar_dano(1)

        # 2. Player toma dano por contato
        hits_contato = pygame.sprite.spritecollide(player, inimigos, False)
        if hits_contato: player.tomar_dano(1)

        # 3. Inimigos tomam dano de projéteis do Player
        acertos = pygame.sprite.groupcollide(inimigos, projeteis_player, False, True)
        for inimigo_atingido in acertos:
            if inimigo_atingido.tomar_dano():
                abates += 1
                if isinstance(inimigo_atingido, InimigoEstatico):
                    fila_respawn_topo.append([agora + 10000, inimigo_atingido.posicao_original])

        # 4. Voadores tomam dano de projéteis
        acertos_v = pygame.sprite.groupcollide(voadores, projeteis_player, False, True)
        for v in acertos_v:
            if v.tomar_dano(): abates += 1

        # Desenho
        u.screen.blit(u.IMG_FUNDO, (0, 0)) 
        sprites.draw(u.screen)
        
        # HUD: Abates e Vida
        txt_abates = u.FONTE_HUD.render(f"ABATES: {abates}", True, u.BLACK)
        txt_vida = u.FONTE_HUD.render(f"VIDA: {player.hp}", True, u.RED)
        u.screen.blit(txt_abates, (50, 50))
        u.screen.blit(txt_vida, (50, 100))
        
        if player.hp <= 0:
            print("GAME OVER")
            rodando = False
        
        pygame.display.flip()
        u.clock.tick(u.FPS)
    pygame.quit()

if __name__ == "__main__":
    main()