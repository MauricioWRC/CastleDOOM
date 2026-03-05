import pygame
import random
import math

import utils as u

class Plataforma(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(u.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(u.BLUE)
        self.rect = self.image.get_rect()
        
        # Posicição inicial
        self.rect.centerx = 960
        self.rect.bottom = 1000
        
        self.vel_y = 0
        self.speed = 9 # Ajustar Velocidade
        self.jump_power = -22 # Ajustar o pulo
        self.gravity = 0.8
        
    def update(self, platforms):
        # Horizontal
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > u.VIRTUAL_WIDTH:
            self.rect.right = u.VIRTUAL_WIDTH
        
        # Gravidade
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        # Colisão com plataformas
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.rect.bottom <= hit.rect.top + self.vel_y:
                    self.rect.bottom = hit.rect.top
                    self.vel_y = 0
                    break
                
    def jump(self, platforms):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel_y = self.jump_power
            
class Inimigo(pygame.sprite.Sprite):
    
    def __init__(self, tipo_spawn):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(u.RED)
        self.rect = self.image.get_rect()
        
        # Posição de spawn
        if tipo_spawn == "chao_esquerda":
            self.rect.x = 50
            self.rect.bottom = 1000
            self.vel_x = 0
        elif tipo_spawn == "chao_direita":
            self.rect.x = u.VIRTUAL_WIDTH - 50
            self.rect.bottom = 1000
            self.vel_x = 0
        elif tipo_spawn == "ceu_esquerda":
            self.rect.x = 400
            self.rect.y = -50
            self.vel_x = 0
        elif tipo_spawn == "ceu_direita":
            self.rect.x = 1400
            self.rect.y = -50
            self.vel_x = 0
            
        self.vel_y = 0
        self.gravity = 0.8
        self.speed = 8
        self.jump_power = -23
        self.jump_cooldown = 0

        
        # Memória de rota da IA
        self.route_target = None

    def get_current_platform_level(self):
        b = self.rect.bottom
        if b >= 995:
            return "ground"
        elif 735 <= b <= 780:
            return "central"
        elif 490 <= b <= 570:
            return "mid"
        elif b <= 220:
            return "top"
        return "air"
    
    def get_player_platform_level(self, player):
        b = player.rect.bottom
        if b >= 995:
            return "ground"
        elif 735 <= b <= 780:
            return "central"
        elif 490 <= b <= 570:
            return "mid"
        elif b <= 220:
            return "top"
        return "air"
        
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

            target_x = player.rect.centerx
            
            # define/atualiza alvo de rota
            if self.route_target is None:
                # Regra 1 e Regra 3 (primeiro passo): chão -> central
                if enemy_level == "ground" and player_level in ("central", "mid"):
                    self.route_target = "central"
                # Regra 2: central -> lado da plataforma média
                elif enemy_level == "central" and player_level == "mid":
                    self.route_target = "mid_left" if player.rect.centerx < CENTRAL_X else "mid_right"

            # executa alvo de rota
            if self.route_target == "central":
                target_x = CENTRAL_X
                if enemy_level == "central":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - CENTRAL_JUMP_X) <= 18:
                    self.jump(platforms)

            elif self.route_target == "mid_left":
                target_x = MID_LEFT_JUMP_X
                if enemy_level == "mid":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - MID_LEFT_JUMP_X) <= 18:
                    self.jump(platforms)

            elif self.route_target == "mid_right":
                target_x = MID_RIGHT_JUMP_X
                if enemy_level == "mid":
                    self.route_target = None
                elif no_chao and self.jump_cooldown == 0 and abs(self.rect.centerx - MID_RIGHT_JUMP_X) <= 18:
                    self.jump(platforms)

            else:
                # perseguição padrão
                if enemy_level == player_level and enemy_level != "air":
                    target_x = player.rect.centerx

            if target_x < self.rect.centerx - 10:
                self.vel_x = -self.speed
            elif target_x > self.rect.centerx + 10:
                self.vel_x = self.speed
            else:
                self.vel_x = 0

        self.rect.x += self.vel_x
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.rect.bottom <= hit.rect.top + self.vel_y:
                    self.rect.bottom = hit.rect.top
                    self.vel_y = 0
                    self.jump_cooldown = 0
                    break
                
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= u.VIRTUAL_WIDTH:
            self.rect.right = u.VIRTUAL_WIDTH
            
        if self.rect.top > u.VIRTUAL_HEIGHT:
            self.kill()
            
    def jump(self, platforms):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if hits:
            self.vel_y = self.jump_power
            self.jump_cooldown = 20

class InimigoVoador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((34, 34), pygame.SRCALPHA)
        self.image.fill(u.GRAY)
        self.rect = self.image.get_rect()

        # Spawn aleatório: acima ou abaixo das plataformas superiores
        side = random.choice(["left", "right"])
        zone = random.choice(["above", "below"])

        if side == "left":
            base_x = random.randint(40, 230)
            if zone == "above":
                base_y = random.randint(70, 140)
            else:
                base_y = random.randint(220, 320)
        else:
            base_x = random.randint(1620, 1880)
            if zone == "above":
                base_y = random.randint(60, 130)
            else:
                base_y = random.randint(210, 320)

        self.base_x = base_x
        self.base_y = base_y
        self.t = random.uniform(0, 2 * math.pi)

        # Parâmetros de movimento em "infinito"
        self.ax = random.randint(45, 75)
        self.ay = random.randint(20, 36)
        self.w = random.uniform(0.045, 0.07)

        self.rect.center = (self.base_x, self.base_y)

    def update(self, *args, **kwargs):
        self.t += self.w
        x = self.base_x + self.ax * math.sin(self.t)
        y = self.base_y + self.ay * math.sin(self.t) * math.cos(self.t)
        self.rect.centerx = int(x)
        self.rect.centery = int(y)

