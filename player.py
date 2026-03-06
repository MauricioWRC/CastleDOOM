import pygame
import math
import utils as u
from projetil import Projetil

class AreaMelee(pygame.sprite.Sprite):
    """Área de dano contínua que segue o rato."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((140, 140), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (200, 200, 200, 150), (70, 70), 70)
        self.rect = self.image.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(u.BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = 960
        self.rect.bottom = 1000
        
        self.vel_y = 0
        self.speed = 9
        self.jump_power = -22
        self.gravity = 0.8
        
        # Status do Jogador
        self.hp = 10
        self.ultimo_tiro = 0
        self.cooldown_tiro = 500
        self.ultimo_dano_recebido = 0
        self.periodo_invencivel = 1000 
        
        # --- Atributos do Ataque Corpo a Corpo ---
        self.area_melee = AreaMelee()
        self.ultimo_dano_melee = 0
        self.cooldown_dano_melee = 500 
        # AQUI DEFINE-SE O DANO! (Antes tirava 1, agora tira 2 de cada vez)
        self.dano_melee = 2 

    def tomar_dano(self, quantidade):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_dano_recebido > self.periodo_invencivel:
            self.hp -= quantidade
            self.ultimo_dano_recebido = agora
            return True
        return False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.rect.x -= self.speed
        if keys[pygame.K_d]: self.rect.x += self.speed
            
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > u.VIRTUAL_WIDTH: self.rect.right = u.VIRTUAL_WIDTH
        
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            for hit in hits:
                if self.rect.bottom <= hit.rect.top + self.vel_y:
                    self.rect.bottom = hit.rect.top
                    self.vel_y = 0
                    break
        
        # Efeito visual de invencibilidade (piscar)
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_dano_recebido < self.periodo_invencivel:
            if (agora // 100) % 2 == 0:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def jump(self, platforms):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.y -= 2
        if hits: self.vel_y = self.jump_power
            
    def atirar(self, target_x, target_y, grupo_sprites, grupo_projeteis):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.ultimo_tiro = agora
            tiro = Projetil(self.rect.centerx, self.rect.centery, target_x, target_y)
            grupo_sprites.add(tiro)
            grupo_projeteis.add(tiro)

    def atacar_melee_continuo(self, mx, my, grupo_sprites, inimigos_terrestres, inimigos_voadores):
        if not self.area_melee.alive():
            grupo_sprites.add(self.area_melee)
            
        dx = mx - self.rect.centerx
        dy = my - self.rect.centery
        angle = math.atan2(dy, dx)
        
        distancia = min(math.hypot(dx, dy), 80) 
        self.area_melee.rect.centerx = self.rect.centerx + math.cos(angle) * distancia
        self.area_melee.rect.centery = self.rect.centery + math.sin(angle) * distancia

        abates = 0
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_dano_melee >= self.cooldown_dano_melee:
            self.ultimo_dano_melee = agora
            
            # --- NOVO: Passamos a variável self.dano_melee para dentro dos parênteses! ---
            for inimigo in inimigos_terrestres:
                if pygame.sprite.collide_rect(self.area_melee, inimigo):
                    if inimigo.tomar_dano(self.dano_melee): abates += 1
            
            for voador in inimigos_voadores:
                if pygame.sprite.collide_rect(self.area_melee, voador):
                    if voador.tomar_dano(self.dano_melee): abates += 1
                    
        return abates

    def parar_melee(self):
        if self.area_melee.alive():
            self.area_melee.kill()