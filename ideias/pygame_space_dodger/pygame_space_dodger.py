"""
Space Dodger - jogo simples em Pygame
Arquivo: pygame_space_dodger.py

Como jogar:
- Use as setas esquerda/direita ou A/D para mover a nave
- Espaço para atirar
- P para pausar
- R para reiniciar após perder

Requisitos: Python 3.8+ e pygame
Instalação: pip install pygame
Executar: python pygame_space_dodger.py

Código criado para ser simples, altamente comentado e fácil de expandir.
"""

import pygame
import random
import math
import sys
from dataclasses import dataclass

# Inicialização básica
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont('dejavusans', 22)
BIG_FONT = pygame.font.SysFont('dejavusans', 48)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 220, 0)

# --------- Configurações de jogo ----------
PLAYER_SPEED = 6
BULLET_SPEED = 10
ENEMY_MIN_SPEED = 2
ENEMY_MAX_SPEED = 5
ENEMY_SPAWN_BASE = 900  # menor valor -> spawn mais frequente (ms)
POWERUP_DURATION = 7000  # ms

# Sons (opcionais; use colisões de som silenciosas se mixer falhar)
def safe_load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

SHOOT_SND = None
HIT_SND = None
LEVELUP_SND = None

# Exemplos: se quiser adicionar sons locais, descomente e coloque arquivos.
# SHOOT_SND = safe_load_sound('shoot.wav')
# HIT_SND = safe_load_sound('hit.wav')
# LEVELUP_SND = safe_load_sound('levelup.wav')


@dataclass
class GameState:
    score: int = 0
    lives: int = 3
    level: int = 1
    running: bool = True
    paused: bool = False
    last_enemy_spawn: int = 0
    enemy_spawn_interval: int = ENEMY_SPAWN_BASE
    last_power_time: int = 0
    power_shield: bool = False
    power_double: bool = False


gstate = GameState()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.surf, GREEN, [(0, 30), (25, 0), (50, 30)])
        self.rect = self.surf.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))
        self.speed = PLAYER_SPEED
        self.last_shot = 0
        self.shot_cooldown = 300  # ms

    def update(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def can_shoot(self):
        return pygame.time.get_ticks() - self.last_shot >= self.shot_cooldown

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.can_shoot():
            self.last_shot = now
            bullets = []
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
            if gstate.power_double:
                bullets.append(Bullet(self.rect.centerx - 18, self.rect.top))
                bullets.append(Bullet(self.rect.centerx + 18, self.rect.top))
            if SHOOT_SND:
                SHOOT_SND.play()
            return bullets
        return []


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((4, 10))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(20, 48)
        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, RED, (size//2, size//2), size//2)
        self.rect = self.surf.get_rect(midtop=(random.randint(0, WIDTH), -size))
        self.speed = random.uniform(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.rot = random.uniform(-3, 3)
        self.angle = 0

    def update(self):
        self.rect.y += self.speed + (gstate.level - 1) * 0.4
        self.angle += self.rot
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    TYPES = ['shield', 'double']

    def __init__(self):
        super().__init__()
        self.type = random.choice(PowerUp.TYPES)
        self.surf = pygame.Surface((26, 26), pygame.SRCALPHA)
        if self.type == 'shield':
            pygame.draw.circle(self.surf, (50, 180, 255), (13, 13), 13)
        else:
            pygame.draw.rect(self.surf, (255, 180, 50), (3, 3, 20, 20))
        self.rect = self.surf.get_rect(midtop=(random.randint(20, WIDTH - 20), -26))
        self.speed = 2.0

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Grupos de sprites
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
power_group = pygame.sprite.Group()


def spawn_enemy():
    e = Enemy()
    enemies_group.add(e)


def spawn_powerup():
    p = PowerUp()
    power_group.add(p)


def reset_game():
    global gstate, enemies_group, bullets_group, power_group, player
    gstate = GameState()
    enemies_group.empty()
    bullets_group.empty()
    power_group.empty()
    player.rect.midbottom = (WIDTH // 2, HEIGHT - 30)


def draw_hud():
    score_surf = FONT.render(f'Score: {gstate.score}', True, WHITE)
    lives_surf = FONT.render(f'Lives: {gstate.lives}', True, WHITE)
    level_surf = FONT.render(f'Level: {gstate.level}', True, WHITE)
    SCREEN.blit(score_surf, (10, 10))
    SCREEN.blit(lives_surf, (10, 36))
    SCREEN.blit(level_surf, (WIDTH - 120, 10))

    if gstate.power_shield:
        remaining = max(0, POWERUP_DURATION - (pygame.time.get_ticks() - gstate.last_power_time))
        t = f'Shield: {remaining//1000}s'
        s = FONT.render(t, True, (120, 220, 255))
        SCREEN.blit(s, (10, 60))
    if gstate.power_double:
        remaining = max(0, POWERUP_DURATION - (pygame.time.get_ticks() - gstate.last_power_time))
        t = f'Multi-shot: {remaining//1000}s'
        s = FONT.render(t, True, (255, 200, 120))
        SCREEN.blit(s, (10, 84))


def handle_collisions():
    # Balas x inimigos
    hits = pygame.sprite.groupcollide(enemies_group, bullets_group, True, True)
    for _ in hits:
        gstate.score += 10
        if HIT_SND:
            HIT_SND.play()

    # Player x inimigo
    enemy_hits = pygame.sprite.spritecollide(player, enemies_group, True)
    for _ in enemy_hits:
        if gstate.power_shield:
            gstate.power_shield = False
        else:
            gstate.lives -= 1
        if HIT_SND:
            HIT_SND.play()

    # Player x powerup
    p_hits = pygame.sprite.spritecollide(player, power_group, True)
    for p in p_hits:
        gstate.last_power_time = pygame.time.get_ticks()
        if p.type == 'shield':
            gstate.power_shield = True
        elif p.type == 'double':
            gstate.power_double = True


def update_level_progress():
    # Simples progressão: a cada 200 pontos avança de nível
    new_level = 1 + gstate.score // 200
    if new_level != gstate.level:
        gstate.level = new_level
        # reduzir intervalo de spawn (com um piso)
        gstate.enemy_spawn_interval = max(200, ENEMY_SPAWN_BASE - (gstate.level - 1) * 80)
        if LEVELUP_SND:
            LEVELUP_SND.play()


def draw_center_text(text, sub=None):
    t = BIG_FONT.render(text, True, WHITE)
    rect = t.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10))
    SCREEN.blit(t, rect)
    if sub:
        s = FONT.render(sub, True, GRAY)
        srect = s.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        SCREEN.blit(s, srect)


def mainloop():
    reset_game()
    running = True
    while running:
        dt = CLOCK.tick(FPS)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gstate.paused = not gstate.paused
                if event.key == pygame.K_r and gstate.lives <= 0:
                    reset_game()
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE and not gstate.paused and gstate.lives > 0:
                    new_bullets = player.shoot()
                    for b in new_bullets:
                        bullets_group.add(b)

        keys = pygame.key.get_pressed()

        if not gstate.paused and gstate.lives > 0:
            player.update(keys)
            bullets_group.update()
            enemies_group.update()
            power_group.update()

            # spawn inimigos baseado em intervalo dinâmico
            if now - gstate.last_enemy_spawn > gstate.enemy_spawn_interval:
                spawn_enemy()
                gstate.last_enemy_spawn = now

            # spawn ocasional de powerups (probabilidade reduzida)
            if random.random() < 0.002:
                spawn_powerup()

            # colisões
            handle_collisions()

            # powerups expiram
            if gstate.power_shield or gstate.power_double:
                if now - gstate.last_power_time > POWERUP_DURATION:
                    gstate.power_shield = False
                    gstate.power_double = False

            # ajuste de nível
            update_level_progress()

            # penalidade se muitos inimigos escaparem? (não implementado)

        # Tela
        SCREEN.fill((8, 10, 20))

        # estrelas de fundo simples
        for i in range(60):
            # usa uma aleatoriedade determinística por frame não é necessário; serve de enfeite
            x = (i * 37) % WIDTH
            y = (i * 61 + now//10) % HEIGHT
            SCREEN.set_at((x, y), (30, 30, 40))

        # desenha sprites
        for s in enemies_group.sprites():
            SCREEN.blit(s.surf, s.rect)
        for b in bullets_group.sprites():
            SCREEN.blit(b.surf, b.rect)
        for p in power_group.sprites():
            SCREEN.blit(p.surf, p.rect)

        # efeito de escudo
        if gstate.power_shield:
            radius = 36
            center = player.rect.center
            pygame.draw.circle(SCREEN, (60, 160, 255, 80), center, radius, 2)

        SCREEN.blit(player.surf, player.rect)

        draw_hud()

        if gstate.paused:
            draw_center_text('PAUSADO', 'Pressione P para continuar')
        elif gstate.lives <= 0:
            draw_center_text('GAME OVER', 'Pressione R para reiniciar ou ESC para sair')
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    mainloop()
