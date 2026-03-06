import pygame
import random
import math
import utils as u

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tipo_spawn):
        super().__init__()
        self.image = u.carregar_imagem("img/inimigo_chao.png", (40, 40), u.RED)
        self.rect = self.image.get_rect()
        self.hp = 2
        if tipo_spawn == "chao_esquerda":
            self.rect.x = 50
            self.rect.bottom = 1000
        else:
            self.rect.x = u.VIRTUAL_WIDTH - 50
            self.rect.bottom = 1000
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.8
        self.speed = 3
        self.jump_power = -23
        self.jump_cooldown = 0
        self.update_timer = 0
        self.current_target_x = self.rect.centerx
        self.route_target = None

    # --- NOVO: Agora aceita a "quantidade" de dano ---
    def tomar_dano(self, quantidade=1):
        self.hp -= quantidade
        if self.hp <= 0:
            self.kill()
            return True # Retorna True se morreu
        return False

    def get_current_platform_level(self):
        b = self.rect.bottom
        if b >= 995: return "ground"
        elif 735 <= b <= 780: return "central"
        elif 490 <= b <= 570: return "mid"
        elif b <= 220: return "top"
        return "air"

    def get_player_platform_level(self, player):
        b = player.rect.bottom
        if b >= 995: return "ground"
        elif 735 <= b <= 780: return "central"
        elif 490 <= b <= 570: return "mid"
        elif b <= 220: return "top"
        return "air"

    def jump(self, platforms):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel_y = self.jump_power
            self.jump_cooldown = 20

    def update(self, platforms, player=None):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        no_chao = len(hits) > 0

        if player:
            enemy_level = self.get_current_platform_level()
            player_level = self.get_player_platform_level(player)

            CENTRAL_X = 960
            CENTRAL_JUMP_X = 960
            MID_LEFT_JUMP_X = 880
            MID_RIGHT_JUMP_X = 1040

            target_x = self.rect.centerx

            if self.route_target is None:
                if enemy_level == "ground" and player_level in ("central", "mid"):
                    self.route_target = "central"
                elif enemy_level == "central" and player_level == "mid":
                    if player.rect.centerx < CENTRAL_X:
                        self.route_target = "mid_left"
                    else:
                        self.route_target = "mid_right"

            if self.route_target == "central":
                target_x = CENTRAL_X
                if enemy_level == "central":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - CENTRAL_JUMP_X) <= 28:
                    self.jump(platforms)

            elif self.route_target == "mid_left":
                target_x = MID_LEFT_JUMP_X
                if enemy_level == "mid":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - MID_LEFT_JUMP_X) <= 28:
                    self.jump(platforms)

            elif self.route_target == "mid_right":
                target_x = MID_RIGHT_JUMP_X
                if enemy_level == "mid":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - MID_RIGHT_JUMP_X) <= 28:
                    self.jump(platforms)

            else:
                if enemy_level == player_level and enemy_level != "air":
                    self.update_timer -= 1
                    if self.update_timer <= 0:
                        self.update_timer = random.randint(25, 55)
                        self.current_target_x = player.rect.centerx + random.randint(-80, 80)
                    target_x = self.current_target_x
                else:
                    target_x = player.rect.centerx

            if target_x < self.rect.centerx - 10: self.vel_x = -self.speed
            elif target_x > self.rect.centerx + 10: self.vel_x = self.speed
            else: self.vel_x = 0

        self.rect.x += self.vel_x
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.jump_cooldown > 0: self.jump_cooldown -= 1

        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.rect.bottom <= hit.rect.top + self.vel_y:
                    self.rect.bottom = hit.rect.top
                    self.vel_y = 0
                    self.jump_cooldown = 0
                    break

        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.right >= u.VIRTUAL_WIDTH: self.rect.right = u.VIRTUAL_WIDTH

class InimigoEstatico(pygame.sprite.Sprite):
    def __init__(self, posicao):
        super().__init__()
        self.image = u.carregar_imagem("img/inimigo_estatico.png", (40, 40), u.RED)
        self.rect = self.image.get_rect()
        self.hp = 2
        self.posicao_original = posicao
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown_tiro = 3000
        if posicao == "topo_esquerda":
            self.rect.centerx = 125
            self.rect.bottom = 180
        else:
            self.rect.centerx = 1760
            self.rect.bottom = 160
        self.vel_y = 0
        self.gravity = 0.8

    # --- NOVO: Agora aceita a "quantidade" de dano ---
    def tomar_dano(self, quantidade=1):
        self.hp -= quantidade
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def update(self, platforms, player=None):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for hit in hits:
            if self.rect.bottom <= hit.rect.top + self.vel_y:
                self.rect.bottom = hit.rect.top
                self.vel_y = 0

        if player:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_tiro > self.cooldown_tiro:
                self.ultimo_tiro = agora
                return "atirar"
        return None

class InimigoVoador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = u.carregar_imagem("img/inimigo_voador.png", (34, 34), u.GRAY)
        self.rect = self.image.get_rect()
        self.hp = 2
        self.base_x = random.randint(300, 1600)
        self.base_y = random.randint(100, 400)
        self.t = random.uniform(0, 6.28)
        self.ax = random.randint(60, 100)
        self.ay = random.randint(30, 50)
        self.w = random.uniform(0.03, 0.05)

    # --- NOVO: Agora aceita a "quantidade" de dano ---
    def tomar_dano(self, quantidade=1):
        self.hp -= quantidade
        if self.hp <= 0:
            self.kill()
            return True
        return False

    def update(self, *args, **kwargs):
        self.t += self.w
        x = self.base_x + self.ax * math.sin(self.t)
        y = self.base_y + self.ay * math.sin(self.t) * math.cos(self.t)
        self.rect.centerx = int(x)
        self.rect.centery = int(y)

