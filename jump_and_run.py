import pygame
import sys
import random
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
JUMP_FORCE = -14
PLAYER_SPEED = 5
ENEMY_SPEED = 1
COIN_SIZE = 15
PLAYER_W, PLAYER_H = 36, 44

# Colors
SKY = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
BLUE = (30, 100, 200)
RED = (200, 40, 40)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
BROWN = (139, 90, 43)
WATER_DARK = (0, 80, 180)
WATER_LIGHT = (30, 120, 220)
WATER_SURFACE = (80, 170, 255)
HERO_YELLOW = (255, 220, 40)
HERO_DARK = (200, 170, 0)
HERO_CHEEK = (230, 80, 60)
HERO_EAR_TIP = (40, 30, 20)
ENEMY_CREAM = (245, 235, 210)
ENEMY_DARK = (180, 160, 120)
ENEMY_BROWN = (130, 90, 50)
ENEMY_KOBAN = (230, 190, 50)
FOX_BROWN = (180, 120, 60)
FOX_CREAM = (240, 220, 180)
FOX_DARK = (120, 70, 30)
FOX_COLLAR = (245, 235, 210)
DRAGON_ORANGE = (240, 130, 40)
DRAGON_WING = (100, 180, 220)
DRAGON_BELLY = (250, 210, 140)
DRAGON_FLAME = (255, 80, 20)
ATTACK_DURATION = 20  # frames the attack is visible
ATTACK_COOLDOWN = 40  # frames between attacks
ATTACK_W = PLAYER_W * 3  # 3x player width
ATTACK_H = 40
THUNDER_YELLOW = (255, 255, 60)
THUNDER_WHITE = (255, 255, 200)
SCHALL_PURPLE = (160, 80, 220)
SCHALL_LIGHT = (200, 150, 255)
EGG_WHITE = (255, 250, 240)
EGG_SHELL = (240, 230, 200)
EGG_RED = (210, 60, 60)
EGG_BLUE = (70, 120, 210)
EGG_SPIKE = (180, 140, 80)
BAT_PURPLE = (130, 80, 170)
BAT_LIGHT = (180, 140, 210)
BAT_WING = (100, 60, 140)
BAT_MOUTH = (220, 80, 100)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_W, PLAYER_H)
        self.vy = 0
        self.on_ground = False
        self.lives = 3
        self.score = 0
        self.facing_right = True
        self.is_fox = False
        self.form = "hero"  # hero, fox, egg, bat
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_rect = None

    def update(self, keys, platforms):
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = PLAYER_SPEED
            self.facing_right = True
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

        self.vy += GRAVITY
        self.rect.x += dx
        self._collide_x(dx, platforms)
        self.rect.y += int(self.vy)
        self._collide_y(platforms)

        # Attack cooldown tick
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            # Update attack rect position to follow player
            if self.facing_right:
                self.attack_rect = pygame.Rect(
                    self.rect.right, self.rect.centery - ATTACK_H // 2,
                    ATTACK_W, ATTACK_H)
            else:
                self.attack_rect = pygame.Rect(
                    self.rect.left - ATTACK_W, self.rect.centery - ATTACK_H // 2,
                    ATTACK_W, ATTACK_H)
        else:
            self.attack_rect = None

    def attack(self):
        if self.attack_cooldown > 0 or self.attack_timer > 0:
            return
        self.attack_timer = ATTACK_DURATION
        self.attack_cooldown = ATTACK_COOLDOWN

    def _collide_x(self, dx, platforms):
        for p in platforms:
            if self.rect.colliderect(p):
                if dx > 0:
                    self.rect.right = p.left
                elif dx < 0:
                    self.rect.left = p.right

    def _collide_y(self, platforms):
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

    def draw(self, surface, cam_x):
        if self.form == "fox":
            self._draw_fox(surface, cam_x)
        elif self.form == "egg":
            self._draw_egg(surface, cam_x)
        elif self.form == "bat":
            self._draw_bat(surface, cam_x)
        else:
            self._draw_hero(surface, cam_x)

    def _draw_fox(self, surface, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        f = 1 if self.facing_right else -1
        cx = x + PLAYER_W // 2

        # Sonic Wave
        self._draw_sonic_wave(surface, cam_x, SCHALL_PURPLE)

        # Fluffy tail
        tail_x = cx - f * 14
        pygame.draw.ellipse(surface, FOX_CREAM, (tail_x - 8, y + 4, 16, 28))
        pygame.draw.ellipse(surface, FOX_DARK, (tail_x - 8, y + 4, 16, 28), 1)

        # Big fluffy ears
        pygame.draw.polygon(surface, FOX_BROWN, [
            (x + 2, y + 8), (x - 2, y - 12), (x + 14, y + 2)
        ])
        pygame.draw.polygon(surface, FOX_BROWN, [
            (x + 22, y + 2), (x + 38, y - 12), (x + 34, y + 8)
        ])
        # Inner ears cream
        pygame.draw.polygon(surface, FOX_CREAM, [
            (x + 3, y + 4), (x + 1, y - 6), (x + 12, y + 2)
        ])
        pygame.draw.polygon(surface, FOX_CREAM, [
            (x + 24, y + 2), (x + 35, y - 6), (x + 33, y + 4)
        ])

        # Body (brown)
        pygame.draw.ellipse(surface, FOX_BROWN, (x + 2, y + 10, 32, 32))
        pygame.draw.ellipse(surface, FOX_DARK, (x + 2, y + 10, 32, 32), 1)

        # Cream chest/collar ruff
        pygame.draw.ellipse(surface, FOX_COLLAR, (x + 6, y + 8, 24, 16))

        # Head
        pygame.draw.ellipse(surface, FOX_BROWN, (x + 4, y + 2, 28, 22))

        # Eyes (big round)
        pygame.draw.circle(surface, BLACK, (cx - 6, y + 12), 4)
        pygame.draw.circle(surface, BLACK, (cx + 6, y + 12), 4)
        pygame.draw.circle(surface, WHITE, (cx - 5 + f, y + 11), 2)
        pygame.draw.circle(surface, WHITE, (cx + 7 + f, y + 11), 2)

        # Nose
        pygame.draw.circle(surface, BLACK, (cx, y + 16), 2)

        # Mouth
        pygame.draw.line(surface, FOX_DARK, (cx, y + 18), (cx - 3, y + 20), 1)
        pygame.draw.line(surface, FOX_DARK, (cx, y + 18), (cx + 3, y + 20), 1)

        # Feet
        pygame.draw.ellipse(surface, FOX_DARK, (x + 5, y + 38, 10, 6))
        pygame.draw.ellipse(surface, FOX_DARK, (x + 21, y + 38, 10, 6))

    def _draw_sonic_wave(self, surface, cam_x, color):
        """Shared sonic wave drawing for Fox/Egg/Bat."""
        if self.attack_timer > 0 and self.attack_rect:
            f = 1 if self.facing_right else -1
            progress = 1.0 - (self.attack_timer / ATTACK_DURATION)
            wave_cx = self.rect.centerx - cam_x + f * 10
            wave_cy = self.rect.centery
            for i in range(4):
                radius = int(20 + (progress * 80) + i * 20)
                alpha = max(0, 180 - i * 40 - int(progress * 80))
                if alpha > 0:
                    arc_color = (color[0], color[1], color[2], alpha)
                    arc_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(arc_surf, arc_color, (radius, radius), radius, 3)
                    surface.blit(arc_surf, (wave_cx - radius, wave_cy - radius))
            glow_r = int(8 + progress * 12)
            glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (color[0], color[1], color[2], int(120 * (1 - progress))),
                               (glow_r, glow_r), glow_r)
            surface.blit(glow_surf, (wave_cx - glow_r, wave_cy - glow_r))

    def _draw_egg(self, surface, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        f = 1 if self.facing_right else -1
        cx = x + PLAYER_W // 2

        # Sonic Wave
        self._draw_sonic_wave(surface, cam_x, EGG_BLUE)

        # Egg shell bottom half
        pygame.draw.ellipse(surface, EGG_SHELL, (x + 2, y + 20, 32, 24))
        pygame.draw.ellipse(surface, EGG_SPIKE, (x + 2, y + 20, 32, 24), 2)
        # Zigzag eggshell edge
        for i in range(5):
            zx = x + 4 + i * 6
            pygame.draw.polygon(surface, EGG_SHELL, [
                (zx, y + 22), (zx + 3, y + 16), (zx + 6, y + 22)
            ])

        # Body (round white, sticks out of egg)
        pygame.draw.ellipse(surface, EGG_WHITE, (x + 4, y + 4, 28, 26))

        # Colored triangle patterns on body
        pygame.draw.polygon(surface, EGG_RED, [
            (x + 10, y + 14), (x + 14, y + 8), (x + 18, y + 14)
        ])
        pygame.draw.polygon(surface, EGG_BLUE, [
            (x + 18, y + 14), (x + 22, y + 8), (x + 26, y + 14)
        ])
        pygame.draw.polygon(surface, EGG_RED, [
            (x + 14, y + 22), (x + 18, y + 16), (x + 22, y + 22)
        ])

        # Head spikes (crown)
        for sx in [cx - 6, cx, cx + 6]:
            pygame.draw.polygon(surface, EGG_SPIKE, [
                (sx - 3, y + 6), (sx, y - 6), (sx + 3, y + 6)
            ])

        # Eyes
        pygame.draw.circle(surface, BLACK, (cx - 5, y + 12), 3)
        pygame.draw.circle(surface, BLACK, (cx + 5, y + 12), 3)
        pygame.draw.circle(surface, WHITE, (cx - 4 + f, y + 11), 1)
        pygame.draw.circle(surface, WHITE, (cx + 6 + f, y + 11), 1)

        # Happy mouth
        pygame.draw.arc(surface, (180, 100, 80), (cx - 4, y + 14, 8, 5), 3.14, 6.28, 1)

        # Little arms/hands poking out of shell
        pygame.draw.ellipse(surface, EGG_WHITE, (x - 2, y + 22, 8, 6))
        pygame.draw.ellipse(surface, EGG_WHITE, (x + 30, y + 22, 8, 6))

    def _draw_bat(self, surface, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        f = 1 if self.facing_right else -1
        cx = x + PLAYER_W // 2

        # Sonic Wave
        self._draw_sonic_wave(surface, cam_x, BAT_PURPLE)

        # Wings (spread out, flapping)
        import math as m
        wing_flap = int(m.sin(pygame.time.get_ticks() * 0.008) * 5)
        # Left wing
        pygame.draw.polygon(surface, BAT_WING, [
            (x + 4, y + 12), (x - 14, y + 2 + wing_flap), (x - 8, y + 22 + wing_flap), (x + 4, y + 24)
        ])
        # Right wing
        pygame.draw.polygon(surface, BAT_WING, [
            (x + 32, y + 12), (x + 50, y + 2 + wing_flap), (x + 44, y + 22 + wing_flap), (x + 32, y + 24)
        ])
        # Wing membrane lines
        pygame.draw.line(surface, BAT_PURPLE, (x + 2, y + 14), (x - 10, y + 8 + wing_flap), 1)
        pygame.draw.line(surface, BAT_PURPLE, (x + 34, y + 14), (x + 46, y + 8 + wing_flap), 1)

        # Body (purple oval)
        pygame.draw.ellipse(surface, BAT_PURPLE, (x + 4, y + 8, 28, 30))
        pygame.draw.ellipse(surface, BAT_WING, (x + 4, y + 8, 28, 30), 2)

        # Head
        pygame.draw.ellipse(surface, BAT_PURPLE, (x + 6, y + 2, 24, 20))

        # Big ears (bat ears)
        pygame.draw.polygon(surface, BAT_PURPLE, [
            (x + 6, y + 6), (x + 2, y - 12), (x + 16, y + 4)
        ])
        pygame.draw.polygon(surface, BAT_PURPLE, [
            (x + 20, y + 4), (x + 34, y - 12), (x + 30, y + 6)
        ])
        # Inner ears
        pygame.draw.polygon(surface, BAT_LIGHT, [
            (x + 8, y + 3), (x + 5, y - 6), (x + 14, y + 3)
        ])
        pygame.draw.polygon(surface, BAT_LIGHT, [
            (x + 22, y + 3), (x + 31, y - 6), (x + 28, y + 3)
        ])

        # No real eyes (blind bat) - just closed slits
        pygame.draw.line(surface, BLACK, (cx - 7, y + 10), (cx - 3, y + 10), 2)
        pygame.draw.line(surface, BLACK, (cx + 3, y + 10), (cx + 7, y + 10), 2)

        # Open mouth with fangs
        pygame.draw.ellipse(surface, BAT_MOUTH, (cx - 5, y + 13, 10, 6))
        pygame.draw.polygon(surface, WHITE, [(cx - 3, y + 13), (cx - 2, y + 17), (cx - 1, y + 13)])
        pygame.draw.polygon(surface, WHITE, [(cx + 1, y + 13), (cx + 2, y + 17), (cx + 3, y + 13)])

        # Small feet
        pygame.draw.ellipse(surface, BAT_PURPLE, (x + 8, y + 36, 8, 6))
        pygame.draw.ellipse(surface, BAT_PURPLE, (x + 20, y + 36, 8, 6))

    def _draw_hero(self, surface, cam_x):
        x = self.rect.x - cam_x
        y = self.rect.y
        f = 1 if self.facing_right else -1
        cx = x + PLAYER_W // 2

        # Draw Lightning Strike attack if active
        if self.attack_timer > 0 and self.attack_rect:
            ax = self.attack_rect.x - cam_x
            ay = self.attack_rect.y
            alpha = self.attack_timer / ATTACK_DURATION
            # Lightning bolts
            for i in range(5):
                bx = ax + i * (ATTACK_W // 5)
                by = ay + random.randint(0, ATTACK_H)
                # Zigzag bolt
                points = [(bx, by)]
                for j in range(3):
                    bx += random.randint(8, 20) * f
                    by += random.randint(-12, 12)
                    points.append((bx, by))
                if len(points) >= 2:
                    pygame.draw.lines(surface, THUNDER_WHITE, False, points, 3)
                    pygame.draw.lines(surface, THUNDER_YELLOW, False, points, 1)
            # Glow effect
            glow_surf = pygame.Surface((ATTACK_W, ATTACK_H), pygame.SRCALPHA)
            glow_surf.fill((255, 255, 60, int(60 * alpha)))
            surface.blit(glow_surf, (ax, ay))

        # Tail (lightning bolt shape behind body)
        tail_x = cx - f * 20
        pygame.draw.polygon(surface, HERO_DARK, [
            (tail_x, y + 10),
            (tail_x - f * 6, y + 2),
            (tail_x - f * 2, y + 8),
            (tail_x - f * 10, y - 2),
            (tail_x - f * 4, y + 6),
            (tail_x - f * 12, y + 4),
            (tail_x - f * 2, y + 14),
        ])

        # Ears (tall pointy triangles)
        pygame.draw.polygon(surface, HERO_YELLOW, [
            (x + 4, y + 8), (x + 2, y - 14), (x + 14, y + 4)
        ])
        pygame.draw.polygon(surface, HERO_EAR_TIP, [
            (x + 3, y - 10), (x + 2, y - 14), (x + 8, y - 4)
        ])
        pygame.draw.polygon(surface, HERO_YELLOW, [
            (x + 22, y + 4), (x + 34, y - 14), (x + 32, y + 8)
        ])
        pygame.draw.polygon(surface, HERO_EAR_TIP, [
            (x + 28, y - 4), (x + 34, y - 14), (x + 33, y - 10)
        ])

        # Body (round yellow)
        pygame.draw.ellipse(surface, HERO_YELLOW, (x + 2, y + 8, 32, 34))
        pygame.draw.ellipse(surface, HERO_DARK, (x + 2, y + 8, 32, 34), 2)

        # Head
        pygame.draw.ellipse(surface, HERO_YELLOW, (x + 4, y + 4, 28, 22))

        # Eyes
        le_x = cx - 7
        re_x = cx + 5
        ey = y + 13
        pygame.draw.circle(surface, BLACK, (le_x, ey), 4)
        pygame.draw.circle(surface, BLACK, (re_x, ey), 4)
        pygame.draw.circle(surface, WHITE, (le_x + f, ey - 1), 2)
        pygame.draw.circle(surface, WHITE, (re_x + f, ey - 1), 2)

        # Nose
        pygame.draw.circle(surface, HERO_DARK, (cx, y + 17), 1)

        # Mouth
        pygame.draw.arc(surface, HERO_DARK, (cx - 4, y + 16, 8, 6), 3.14, 6.28, 1)

        # Red cheeks
        pygame.draw.circle(surface, HERO_CHEEK, (x + 5, y + 18), 4)
        pygame.draw.circle(surface, HERO_CHEEK, (x + 31, y + 18), 4)

        # Feet
        pygame.draw.ellipse(surface, HERO_DARK, (x + 5, y + 38, 10, 6))
        pygame.draw.ellipse(surface, HERO_DARK, (x + 21, y + 38, 10, 6))


class Enemy:
    def __init__(self, x, y, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = ENEMY_SPEED
        self.alive = True

    def update(self):
        if not self.alive:
            return
        self.rect.x += self.speed
        if self.rect.x <= self.left_bound or self.rect.right >= self.right_bound:
            self.speed *= -1

    def draw(self, surface, cam_x):
        if not self.alive:
            return
        x = self.rect.x - cam_x
        y = self.rect.y
        cx = x + 15  # center
        facing = 1 if self.speed >= 0 else -1

        # Curly tail
        tail_x = cx - facing * 16
        pygame.draw.arc(surface, ENEMY_DARK,
                        (tail_x - 6, y - 4, 14, 18), 0.5, 4.5, 2)

        # Body (cream oval)
        pygame.draw.ellipse(surface, ENEMY_CREAM, (x + 3, y + 8, 24, 22))
        pygame.draw.ellipse(surface, ENEMY_DARK, (x + 3, y + 8, 24, 22), 1)

        # Head (cream circle)
        pygame.draw.ellipse(surface, ENEMY_CREAM, (x + 1, y + 0, 28, 20))

        # Ears (pointed cat ears)
        pygame.draw.polygon(surface, ENEMY_CREAM, [
            (x + 2, y + 6), (x + 0, y - 6), (x + 10, y + 2)
        ])
        pygame.draw.polygon(surface, ENEMY_CREAM, [
            (x + 20, y + 2), (x + 30, y - 6), (x + 28, y + 6)
        ])
        # Inner ears (dark)
        pygame.draw.polygon(surface, ENEMY_BROWN, [
            (x + 3, y + 3), (x + 2, y - 3), (x + 9, y + 2)
        ])
        pygame.draw.polygon(surface, ENEMY_BROWN, [
            (x + 21, y + 2), (x + 28, y - 3), (x + 27, y + 3)
        ])

        # Koban coin on forehead
        pygame.draw.ellipse(surface, ENEMY_KOBAN, (cx - 4, y + 2, 8, 6))
        pygame.draw.ellipse(surface, ENEMY_BROWN, (cx - 4, y + 2, 8, 6), 1)

        # Eyes (slit cat eyes)
        pygame.draw.ellipse(surface, WHITE, (x + 5, y + 9, 8, 6))
        pygame.draw.ellipse(surface, WHITE, (x + 17, y + 9, 8, 6))
        pygame.draw.ellipse(surface, BLACK, (x + 8, y + 10, 3, 5))
        pygame.draw.ellipse(surface, BLACK, (x + 20, y + 10, 3, 5))

        # Nose + mouth
        pygame.draw.circle(surface, (220, 140, 140), (cx, y + 14), 2)
        pygame.draw.line(surface, ENEMY_DARK, (cx, y + 15), (cx - 3, y + 17), 1)
        pygame.draw.line(surface, ENEMY_DARK, (cx, y + 15), (cx + 3, y + 17), 1)

        # Whiskers (3 per side)
        pygame.draw.line(surface, ENEMY_DARK, (x + 4, y + 13), (x - 6, y + 10), 1)
        pygame.draw.line(surface, ENEMY_DARK, (x + 4, y + 15), (x - 7, y + 15), 1)
        pygame.draw.line(surface, ENEMY_DARK, (x + 4, y + 17), (x - 6, y + 20), 1)
        pygame.draw.line(surface, ENEMY_DARK, (x + 26, y + 13), (x + 36, y + 10), 1)
        pygame.draw.line(surface, ENEMY_DARK, (x + 26, y + 15), (x + 37, y + 15), 1)
        pygame.draw.line(surface, ENEMY_DARK, (x + 26, y + 17), (x + 36, y + 20), 1)

        # Feet
        pygame.draw.ellipse(surface, ENEMY_CREAM, (x + 4, y + 26, 9, 5))
        pygame.draw.ellipse(surface, ENEMY_CREAM, (x + 17, y + 26, 9, 5))
        pygame.draw.ellipse(surface, ENEMY_DARK, (x + 4, y + 26, 9, 5), 1)
        pygame.draw.ellipse(surface, ENEMY_DARK, (x + 17, y + 26, 9, 5), 1)


class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, COIN_SIZE, COIN_SIZE)
        self.collected = False
        self.bob_offset = random.uniform(0, 6.28)

    def draw(self, surface, cam_x, tick):
        if self.collected:
            return
        bob = int(math.sin(tick * 0.05 + self.bob_offset) * 3)
        x = self.rect.x - cam_x
        y = self.rect.y + bob
        pygame.draw.circle(surface, YELLOW, (x + COIN_SIZE // 2, y + COIN_SIZE // 2), COIN_SIZE // 2)
        pygame.draw.circle(surface, (200, 170, 0), (x + COIN_SIZE // 2, y + COIN_SIZE // 2), COIN_SIZE // 2, 2)


class Cloud:
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

    def draw(self, surface, cam_x):
        x = self.x - cam_x * 0.3  # Parallax
        pygame.draw.ellipse(surface, WHITE, (int(x), self.y, self.w, 30))
        pygame.draw.ellipse(surface, WHITE, (int(x) + 15, self.y - 12, self.w - 20, 30))


class Water:
    def __init__(self, x, w, y_top):
        self.rect = pygame.Rect(x, y_top, w, HEIGHT - y_top)
        self.x = x
        self.w = w
        self.y_top = y_top

    def draw(self, surface, cam_x, tick):
        x = self.x - cam_x
        # Water body
        pygame.draw.rect(surface, WATER_DARK, (x, self.y_top, self.w, HEIGHT - self.y_top))
        # Animated waves on surface
        for wx in range(0, self.w, 20):
            wave_y = self.y_top + int(math.sin(tick * 0.08 + wx * 0.15) * 3)
            pygame.draw.ellipse(surface, WATER_SURFACE, (x + wx, wave_y - 4, 24, 8))
        # Lighter band near surface
        pygame.draw.rect(surface, WATER_LIGHT, (x, self.y_top, self.w, 12))


class FoxItem:
    """Collectible E that transforms hero into Fox."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False
        self.bob_offset = 0

    def draw(self, surface, cam_x, tick):
        if self.collected:
            return
        bob = int(math.sin(tick * 0.04) * 4)
        x = self.rect.x - cam_x
        y = self.rect.y + bob
        # Glowing circle background
        glow = 120 + int(math.sin(tick * 0.06) * 40)
        pygame.draw.circle(surface, (glow, 255, glow), (x + 12, y + 12), 16)
        pygame.draw.circle(surface, FOX_BROWN, (x + 12, y + 12), 13)
        # Letter E
        font = pygame.font.SysFont("consolas", 20, bold=True)
        letter = font.render("E", True, WHITE)
        surface.blit(letter, (x + 5, y + 2))


class EggItem:
    """Collectible T that transforms into Egg."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False

    def draw(self, surface, cam_x, tick):
        if self.collected:
            return
        bob = int(math.sin(tick * 0.04 + 1.5) * 4)
        x = self.rect.x - cam_x
        y = self.rect.y + bob
        glow = 120 + int(math.sin(tick * 0.06 + 1.5) * 40)
        pygame.draw.circle(surface, (glow, glow, 255), (x + 12, y + 12), 16)
        pygame.draw.circle(surface, EGG_BLUE, (x + 12, y + 12), 13)
        font = pygame.font.SysFont("consolas", 20, bold=True)
        letter = font.render("T", True, WHITE)
        surface.blit(letter, (x + 5, y + 2))


class BatItem:
    """Collectible B that transforms into Bat."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.collected = False

    def draw(self, surface, cam_x, tick):
        if self.collected:
            return
        bob = int(math.sin(tick * 0.04 + 3.0) * 4)
        x = self.rect.x - cam_x
        y = self.rect.y + bob
        glow = 120 + int(math.sin(tick * 0.06 + 3.0) * 40)
        pygame.draw.circle(surface, (glow, 120, 255), (x + 12, y + 12), 16)
        pygame.draw.circle(surface, BAT_PURPLE, (x + 12, y + 12), 13)
        font = pygame.font.SysFont("consolas", 20, bold=True)
        letter = font.render("B", True, WHITE)
        surface.blit(letter, (x + 5, y + 2))


class Dragon:
    """Flying Charizard platform that moves back and forth over the summit gap."""
    def __init__(self, x, y, left_bound, right_bound):
        self.x = float(x)
        self.y = float(y)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.speed = 1.5
        self.w = 70
        self.h = 16  # platform collision height
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.x += self.speed
        if self.x <= self.left_bound or self.x + self.w >= self.right_bound:
            self.speed *= -1
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, surface, cam_x, tick):
        x = int(self.x) - cam_x
        y = int(self.y)
        facing = 1 if self.speed >= 0 else -1
        cx = x + self.w // 2

        # Wings (large, spread out)
        wing_flap = int(math.sin(tick * 0.12) * 5)
        # Left wing
        pygame.draw.polygon(surface, DRAGON_WING, [
            (cx - 10, y + 4), (x - 15, y - 18 + wing_flap), (x + 5, y - 2)
        ])
        # Right wing
        pygame.draw.polygon(surface, DRAGON_WING, [
            (cx + 10, y + 4), (x + self.w + 15, y - 18 + wing_flap), (x + self.w - 5, y - 2)
        ])

        # Body (orange oval)
        pygame.draw.ellipse(surface, DRAGON_ORANGE, (x + 10, y - 6, 50, 26))
        pygame.draw.ellipse(surface, (200, 100, 20), (x + 10, y - 6, 50, 26), 2)

        # Belly
        pygame.draw.ellipse(surface, DRAGON_BELLY, (x + 20, y, 30, 14))

        # Head
        hx = cx + facing * 20
        pygame.draw.ellipse(surface, DRAGON_ORANGE, (hx - 10, y - 14, 22, 18))
        # Eyes
        pygame.draw.circle(surface, WHITE, (hx + facing * 3, y - 7), 4)
        pygame.draw.circle(surface, BLACK, (hx + facing * 4, y - 7), 2)
        # Mouth / snout
        pygame.draw.ellipse(surface, (220, 120, 40), (hx + facing * 6, y - 6, 8, 5))

        # Tail flame
        tail_x = cx - facing * 28
        flame_flicker = int(math.sin(tick * 0.2) * 3)
        pygame.draw.polygon(surface, DRAGON_FLAME, [
            (tail_x, y + 4), (tail_x - facing * 12, y - 4 + flame_flicker),
            (tail_x - facing * 6, y + 8)
        ])
        pygame.draw.polygon(surface, YELLOW, [
            (tail_x, y + 4), (tail_x - facing * 7, y - 1 + flame_flicker),
            (tail_x - facing * 3, y + 6)
        ])


class Flag:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y - 60, 10, 60)
        self.x = x
        self.y = y

    def draw(self, surface, cam_x):
        x = self.x - cam_x
        pygame.draw.rect(surface, GRAY, (x, self.y - 60, 5, 60))
        pygame.draw.polygon(surface, RED, [(x + 5, self.y - 60), (x + 35, self.y - 48), (x + 5, self.y - 36)])


def build_level():
    platforms = []
    enemies = []
    coins = []
    GROUND = HEIGHT - 40  # 560 = top of ground level
    STEP_H = 50           # height per step (easily jumpable, max jump ~122px)
    STEP_W = 250          # width of each step

    # === MOUNTAIN LEVEL LAYOUT ===
    # Flat start → 6 ascending steps → summit → water gap → summit → 6 descending steps → flat end → flag

    # --- Flat start area (split for water gap) ---
    platforms.append(pygame.Rect(0, GROUND, 500, 40))
    platforms.append(pygame.Rect(620, GROUND, 280, 40))  # after water gap

    # --- Water gap near the start ---
    water_zones = [Water(500, 120, GROUND)]

    # --- Ascending steps (left side of mountain) ---
    ascent_steps = []
    for i in range(6):
        sx = 900 + i * STEP_W
        sy = GROUND - (i + 1) * STEP_H
        sh = (i + 1) * STEP_H + 40
        ascent_steps.append((sx, sy, STEP_W, sh))
        platforms.append(pygame.Rect(sx, sy, STEP_W, sh))

    # --- Summit platforms (both sides of wider gap) ---
    summit_y = GROUND - 7 * STEP_H
    summit_left_x = 900 + 6 * STEP_W     # 2400
    summit_gap_w = 400                     # wider gap for dragon
    summit_right_x = summit_left_x + 300 + summit_gap_w  # 3100
    summit_h = 7 * STEP_H + 40

    platforms.append(pygame.Rect(summit_left_x, summit_y, 300, summit_h))  # left summit
    platforms.append(pygame.Rect(summit_right_x, summit_y, 300, summit_h))  # right summit

    # --- Flying dragon platform in summit gap ---
    dragon_gap_left = summit_left_x + 300
    dragon_gap_right = summit_right_x
    dragon = Dragon(dragon_gap_left + 50, summit_y + 20,
                    dragon_gap_left, dragon_gap_right)

    # --- Descending steps (right side of mountain) ---
    descent_start_x = summit_right_x + 300  # 3400
    for i in range(6):
        sx = descent_start_x + i * STEP_W
        sy = GROUND - (6 - i) * STEP_H
        sh = (6 - i) * STEP_H + 40
        platforms.append(pygame.Rect(sx, sy, STEP_W, sh))

    # --- Flat end area ---
    flat_end_x = descent_start_x + 6 * STEP_W
    platforms.append(pygame.Rect(flat_end_x, GROUND, 900, 40))

    # --- Enemies ---
    # descent step tops: step i has y = GROUND - (6-i)*STEP_H
    enemy_data = [
        # Flat start area
        (200, GROUND - 30, 100, 480),
        (700, GROUND - 30, 640, 880),
        # On ascending steps
        (1000, GROUND - STEP_H - 30, 920, 1130),
        (1550, GROUND - 3 * STEP_H - 30, 1520, 1630),
        (2100, GROUND - 5 * STEP_H - 30, 2070, 2200),
        # On summits
        (2450, summit_y - 30, 2420, 2680),
        (summit_right_x + 50, summit_y - 30, summit_right_x + 20, summit_right_x + 280),
        # On descending steps (correct y position for each step)
        (descent_start_x + 50, GROUND - 6 * STEP_H - 30, descent_start_x + 20, descent_start_x + 230),
        (descent_start_x + 2 * STEP_W + 50, GROUND - 4 * STEP_H - 30, descent_start_x + 2 * STEP_W + 20, descent_start_x + 2 * STEP_W + 230),
        (descent_start_x + 4 * STEP_W + 50, GROUND - 2 * STEP_H - 30, descent_start_x + 4 * STEP_W + 20, descent_start_x + 4 * STEP_W + 230),
        # Flat end area
        (flat_end_x + 200, GROUND - 30, flat_end_x + 100, flat_end_x + 500),
        (flat_end_x + 600, GROUND - 30, flat_end_x + 500, flat_end_x + 800),
    ]
    for x, y, lb, rb in enemy_data:
        enemies.append(Enemy(x, y, lb, rb))

    # --- Transform items ---
    fox_item = FoxItem(1700, GROUND - 4 * STEP_H - 50)
    egg_item = EggItem(2500, summit_y - 50)  # on left summit
    bat_item = BatItem(descent_start_x + 2 * STEP_W + 100, GROUND - 4 * STEP_H - 50)  # mid descent

    # --- Coins along the mountain path ---
    coin_positions = [
        # Flat start
        (150, GROUND - 30), (250, GROUND - 30), (380, GROUND - 30),
        (700, GROUND - 30), (780, GROUND - 30),
        # Ascending - coins on each step edge
        (950, GROUND - STEP_H - 30), (1020, GROUND - STEP_H - 30),
        (1200, GROUND - 2 * STEP_H - 30), (1270, GROUND - 2 * STEP_H - 30),
        (1450, GROUND - 3 * STEP_H - 30), (1520, GROUND - 3 * STEP_H - 30),
        (1700, GROUND - 4 * STEP_H - 30), (1770, GROUND - 4 * STEP_H - 30),
        (1950, GROUND - 5 * STEP_H - 30), (2020, GROUND - 5 * STEP_H - 30),
        (2200, GROUND - 6 * STEP_H - 30), (2270, GROUND - 6 * STEP_H - 30),
        # Summit coins
        (2500, summit_y - 30), (2600, summit_y - 30),
        (summit_right_x + 50, summit_y - 30), (summit_right_x + 150, summit_y - 30),
        # Descending
        (descent_start_x + 50, GROUND - 6 * STEP_H - 30),
        (descent_start_x + 120, GROUND - 6 * STEP_H - 30),
        (descent_start_x + STEP_W + 50, GROUND - 5 * STEP_H - 30),
        (descent_start_x + STEP_W + 120, GROUND - 5 * STEP_H - 30),
        (descent_start_x + 2 * STEP_W + 50, GROUND - 4 * STEP_H - 30),
        (descent_start_x + 2 * STEP_W + 120, GROUND - 4 * STEP_H - 30),
        (descent_start_x + 3 * STEP_W + 50, GROUND - 3 * STEP_H - 30),
        (descent_start_x + 3 * STEP_W + 120, GROUND - 3 * STEP_H - 30),
        (descent_start_x + 4 * STEP_W + 50, GROUND - 2 * STEP_H - 30),
        (descent_start_x + 4 * STEP_W + 120, GROUND - 2 * STEP_H - 30),
        (descent_start_x + 5 * STEP_W + 50, GROUND - STEP_H - 30),
        (descent_start_x + 5 * STEP_W + 120, GROUND - STEP_H - 30),
        # Flat end
        (flat_end_x + 100, GROUND - 30), (flat_end_x + 200, GROUND - 30),
        (flat_end_x + 400, GROUND - 30),
    ]
    for x, y in coin_positions:
        coins.append(Coin(x, y))

    # --- Flag at the end ---
    flag = Flag(flat_end_x + 700, GROUND)
    clouds = [Cloud(random.randint(0, 6000), random.randint(20, 120), random.randint(60, 120)) for _ in range(20)]

    return platforms, enemies, coins, flag, clouds, water_zones, dragon, fox_item, egg_item, bat_item


def draw_text(surface, text, size, x, y, color=WHITE, center=False):
    font = pygame.font.SysFont("consolas", size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)


def title_screen(surface, clock):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

        surface.fill(SKY)
        draw_text(surface, "JUMP & RUN", 56, WIDTH // 2, 180, BLUE, center=True)
        draw_text(surface, "Arrow Keys / WASD to move", 22, WIDTH // 2, 300, BLACK, center=True)
        draw_text(surface, "Space / Up / W to jump", 22, WIDTH // 2, 340, BLACK, center=True)
        draw_text(surface, "Stomp enemies from above!", 22, WIDTH // 2, 380, RED, center=True)
        draw_text(surface, "F = Lightning / Sonic Wave attack!", 22, WIDTH // 2, 410, (160, 80, 220), center=True)
        draw_text(surface, "Collect coins & reach the flag!", 22, WIDTH // 2, 440, DARK_GREEN, center=True)
        draw_text(surface, "Press any key to start", 26, WIDTH // 2, 520, GRAY, center=True)

        pygame.display.flip()
        clock.tick(FPS)


def game_over_screen(surface, clock, score, won):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        surface.fill(SKY if won else (40, 40, 60))
        msg = "YOU WIN!" if won else "GAME OVER"
        color = DARK_GREEN if won else RED
        draw_text(surface, msg, 56, WIDTH // 2, 200, color, center=True)
        draw_text(surface, f"Score: {score}", 30, WIDTH // 2, 300, WHITE if not won else BLACK, center=True)
        draw_text(surface, "R = Restart   Q = Quit", 24, WIDTH // 2, 420, GRAY, center=True)

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jump & Run")
    clock = pygame.time.Clock()

    title_screen(screen, clock)

    while True:  # Restart loop
        player = Player(50, HEIGHT - 120)
        platforms, enemies, coins, flag, clouds, water_zones, dragon, fox_item, egg_item, bat_item = build_level()
        tick = 0
        running = True
        won = False

        while running:
            tick += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    player.attack()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

            # Update dragon (moving platform)
            dragon.update()

            player.update(keys, platforms + [dragon.rect])

            for enemy in enemies:
                enemy.update()

            # Player-enemy collision
            for enemy in enemies:
                if not enemy.alive:
                    continue
                # Attack kills enemy
                if player.attack_rect and player.attack_timer > 0:
                    if enemy.rect.colliderect(player.attack_rect):
                        enemy.alive = False
                        player.score += 100
                        continue
                if player.rect.colliderect(enemy.rect):
                    if player.vy > 0 and player.rect.bottom - enemy.rect.top < 20:
                        enemy.alive = False
                        player.vy = JUMP_FORCE * 0.6
                        player.score += 100
                    else:
                        player.lives -= 1
                        if player.lives <= 0:
                            running = False
                        else:
                            player.rect.x = 50
                            player.rect.y = HEIGHT - 120
                            player.vy = 0

            # Coin collection
            for coin in coins:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collected = True
                    player.score += 50

            # Fox item collection
            if not fox_item.collected and player.rect.colliderect(fox_item.rect):
                fox_item.collected = True
                player.is_fox = True
                player.form = "fox"
                player.score += 200

            # Egg item collection
            if not egg_item.collected and player.rect.colliderect(egg_item.rect):
                egg_item.collected = True
                player.form = "egg"
                player.score += 200

            # Bat item collection
            if not bat_item.collected and player.rect.colliderect(bat_item.rect):
                bat_item.collected = True
                player.form = "bat"
                player.score += 200

            # Water collision — touching water kills like falling
            for wz in water_zones:
                if player.rect.colliderect(wz.rect):
                    player.lives -= 1
                    if player.lives <= 0:
                        running = False
                    else:
                        player.rect.x = 50
                        player.rect.y = HEIGHT - 120
                        player.vy = 0
                    break

            # Fall off screen
            if player.rect.top > HEIGHT + 100:
                player.lives -= 1
                if player.lives <= 0:
                    running = False
                else:
                    player.rect.x = 50
                    player.rect.y = HEIGHT - 120
                    player.vy = 0

            # Reach flag
            if player.rect.colliderect(flag.rect):
                won = True
                running = False

            # Camera
            cam_x = player.rect.centerx - WIDTH // 3
            cam_x = max(0, cam_x)

            # --- Draw ---
            screen.fill(SKY)

            # Background mountains
            for i in range(6):
                mx = i * 350 - int(cam_x * 0.15) % 2100
                pygame.draw.polygon(screen, (100, 140, 100), [
                    (mx, HEIGHT - 40), (mx + 175, HEIGHT - 220), (mx + 350, HEIGHT - 40)
                ])

            for cloud in clouds:
                cloud.draw(screen, cam_x)

            # Platforms
            for p in platforms:
                r = pygame.Rect(p.x - cam_x, p.y, p.width, p.height)
                if p.height >= 40:  # Ground
                    pygame.draw.rect(screen, GREEN, r)
                    pygame.draw.rect(screen, DARK_GREEN, r, 2)
                    # Grass tufts
                    for gx in range(r.left, r.right, 20):
                        pygame.draw.line(screen, DARK_GREEN, (gx, r.top), (gx - 3, r.top - 6), 2)
                        pygame.draw.line(screen, DARK_GREEN, (gx, r.top), (gx + 3, r.top - 6), 2)
                else:  # Floating
                    pygame.draw.rect(screen, BROWN, r)
                    pygame.draw.rect(screen, (100, 60, 20), r, 2)
                    pygame.draw.rect(screen, GREEN, (r.x, r.y, r.width, 5))

            # Water zones (draw behind entities)
            for wz in water_zones:
                wz.draw(screen, cam_x, tick)

            # Dragon (flying platform)
            dragon.draw(screen, cam_x, tick)

            # Fox item
            fox_item.draw(screen, cam_x, tick)
            egg_item.draw(screen, cam_x, tick)
            bat_item.draw(screen, cam_x, tick)

            for coin in coins:
                coin.draw(screen, cam_x, tick)

            for enemy in enemies:
                enemy.draw(screen, cam_x)

            flag.draw(screen, cam_x)
            player.draw(screen, cam_x)

            # HUD
            pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, WIDTH, 36))
            draw_text(screen, f"Score: {player.score}", 20, 15, 8, YELLOW)
            draw_text(screen, f"Lives: {'<3 ' * player.lives}", 20, 200, 8, RED)

            pygame.display.flip()
            clock.tick(FPS)

        result = game_over_screen(screen, clock, player.score, won)
        if result != "restart":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
