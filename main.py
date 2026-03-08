import pygame
import random
import utils as u
from plataforma import Plataforma
from player import Player
from inimigos import Inimigo, InimigoVoador, InimigoEstatico
from projetil import ProjetilInimigo


def criar_estado_jogo():
    sprites = pygame.sprite.Group()
    platformas = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    voadores = pygame.sprite.Group()
    projeteis_player = pygame.sprite.Group()
    projeteis_inimigos = pygame.sprite.Group()

    # Configuracao de plataformas
    lista_plataformas = [
        (0, 1000, 1920, 80),
        (860, 750, 200, 20),
        (300, 550, 300, 20),
        (1300, 500, 350, 20),
        (0, 180, 250, 20),
        (1600, 160, 320, 20),
    ]
    for plat in lista_plataformas:
        p = Plataforma(*plat)
        sprites.add(p)
        platformas.add(p)

    player = Player()
    sprites.add(player)

    # Guardas iniciais
    for pos in ["topo_esquerda", "topo_direita"]:
        g = InimigoEstatico(pos)
        sprites.add(g)
        inimigos.add(g)

    estado = {
        "sprites": sprites,
        "platformas": platformas,
        "inimigos": inimigos,
        "voadores": voadores,
        "projeteis_player": projeteis_player,
        "projeteis_inimigos": projeteis_inimigos,
        "player": player,
        "abates": 0,
        "fila_respawn_topo": [],
        "ultimo_spawn_chao": pygame.time.get_ticks(),
        "ultimo_spawn_voador": pygame.time.get_ticks(),
    }
    return estado


def desenhar_tela_game_over(abates):
    overlay = pygame.Surface((u.VIRTUAL_WIDTH, u.VIRTUAL_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    u.screen.blit(overlay, (0, 0))

    fonte_titulo = pygame.font.SysFont("Arial", 110, bold=True)
    fonte_hud = pygame.font.SysFont("Arial", 54, bold=True)
    fonte_instrucao = pygame.font.SysFont("Arial", 40, bold=False)

    txt_game_over = fonte_titulo.render("GAME OVER", True, (220, 40, 40))
    txt_abates = fonte_hud.render(f"ABATES: {abates}", True, u.WHITE)
    txt_instr = fonte_instrucao.render("R ou ENTER para jogar de novo | ESC para sair", True, u.WHITE)

    rect_go = txt_game_over.get_rect(center=(u.VIRTUAL_WIDTH // 2, u.VIRTUAL_HEIGHT // 2 - 120))
    rect_ab = txt_abates.get_rect(center=(u.VIRTUAL_WIDTH // 2, u.VIRTUAL_HEIGHT // 2 - 10))
    rect_in = txt_instr.get_rect(center=(u.VIRTUAL_WIDTH // 2, u.VIRTUAL_HEIGHT // 2 + 90))

    u.screen.blit(txt_game_over, rect_go)
    u.screen.blit(txt_abates, rect_ab)
    u.screen.blit(txt_instr, rect_in)


def loop_game_over(abates):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                if evento.key in (pygame.K_r, pygame.K_RETURN):
                    return True

        desenhar_tela_game_over(abates)
        pygame.display.flip()
        u.clock.tick(u.FPS)


def main():
    executando = True

    while executando:
        estado = criar_estado_jogo()
        rodando = True

        while rodando:
            agora = pygame.time.get_ticks()

            sprites = estado["sprites"]
            platformas = estado["platformas"]
            inimigos = estado["inimigos"]
            voadores = estado["voadores"]
            projeteis_player = estado["projeteis_player"]
            projeteis_inimigos = estado["projeteis_inimigos"]
            player = estado["player"]

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                    rodando = False
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        executando = False
                        rodando = False
                    if evento.key in (pygame.K_SPACE, pygame.K_w):
                        player.jump(platformas)
                        

            if not rodando:
                break

            # Controles do rato
            botoes_rato = pygame.mouse.get_pressed()
            mx, my = pygame.mouse.get_pos()

            # Atirar
            if botoes_rato[0]:
                player.atirar(mx, my, sprites, projeteis_player)

            # Melee continuo
            if botoes_rato[2]:
                novos_abates = player.atacar_melee_continuo(mx, my, sprites, inimigos, voadores)
                estado["abates"] += novos_abates
            else:
                player.parar_melee()

            # Respawn topo
            for item in estado["fila_respawn_topo"][:]:
                if agora >= item[0]:
                    novo = InimigoEstatico(item[1])
                    sprites.add(novo)
                    inimigos.add(novo)
                    estado["fila_respawn_topo"].remove(item)

            # Spawn chao
            if agora - estado["ultimo_spawn_chao"] > 2000:
                e = Inimigo(random.choice(["chao_esquerda", "chao_direita"]))
                sprites.add(e)
                inimigos.add(e)
                estado["ultimo_spawn_chao"] = agora

            # Spawn voador
            if agora - estado["ultimo_spawn_voador"] > 4500:
                v = InimigoVoador()
                sprites.add(v)
                voadores.add(v)
                estado["ultimo_spawn_voador"] = agora

            # Atualizacoes
            player.update(platformas)

            for inimigo in inimigos:
                acao = inimigo.update(platformas, player)
                if acao == "atirar":
                    tiro_i = ProjetilInimigo(
                        inimigo.rect.centerx,
                        inimigo.rect.centery,
                        player.rect.centerx,
                        player.rect.centery,
                    )
                    sprites.add(tiro_i)
                    projeteis_inimigos.add(tiro_i)

            voadores.update()
            projeteis_player.update()
            projeteis_inimigos.update()

            # Colisoes
            if pygame.sprite.spritecollide(player, projeteis_inimigos, True):
                player.tomar_dano(1)

            hits_contato = pygame.sprite.spritecollide(player, inimigos, False)
            if hits_contato:
                player.tomar_dano(1)

            acertos = pygame.sprite.groupcollide(inimigos, projeteis_player, False, True)
            for inimigo_atingido in acertos:
                if inimigo_atingido.tomar_dano():
                    estado["abates"] += 1
                    if isinstance(inimigo_atingido, InimigoEstatico):
                        estado["fila_respawn_topo"].append([agora + 10000, inimigo_atingido.posicao_original])

            acertos_v = pygame.sprite.groupcollide(voadores, projeteis_player, False, True)
            for v in acertos_v:
                if v.tomar_dano():
                    estado["abates"] += 1

            # Desenho
            u.screen.blit(u.IMG_FUNDO, (0, 0))
            sprites.draw(u.screen)

            txt_abates = u.FONTE_HUD.render(f"ABATES: {estado['abates']}", True, u.BLACK)
            txt_vida = u.FONTE_HUD.render(f"VIDA: {player.hp}", True, u.RED)
            u.screen.blit(txt_abates, (50, 50))
            u.screen.blit(txt_vida, (50, 100))

            if player.hp <= 0:
                player.parar_melee()
                rodando = False

            pygame.display.flip()
            u.clock.tick(u.FPS)

        if not executando:
            break

        # Tela de game over com replay
        quer_replay = loop_game_over(estado["abates"])
        if not quer_replay:
            executando = False

    pygame.quit()


if __name__ == "__main__":
    main()