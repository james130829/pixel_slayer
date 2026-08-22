import pygame
import random

pygame.init()

game_font = pygame.font.Font(None, 60)
WHITE = (255,255,255)
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

HEAL_DROP_CHANCE = 0.3
MAX_HEAL = 3
MAX_LIVES = 5

HASTE_DROP_CHANCE = 0.3
MAX_HASTE = 1
HASTE_DURATION = 10 * FPS

SHIELD_DROP_CHANCE = 0.3
MAX_SHIELD = 1
SHIELD_DURATION = 5 * FPS

# 여기 작업 중 !! (스코어 우상단에 그리기)
cell_text = game_font.render(str(self.attack_cooldown), True, WHITE)
text_rect = (screen_width-100,screen_height-100)
screen.blit(cell_text, text_rect)

def draw_score(score):
    (30,350)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 20, 40, 40)
        self.speed = 5
        self.lives = 3

        self.attack_range = pygame.Rect(self.rect.x -40, self.rect.y -40, 120, 120)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.attack_cooldown_base = 3 * FPS
        self.attack_cooldown_max = self.attack_cooldown_base
        self.haste_timer = 0
        self.shield_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            if self.rect.x < 0:
                self.rect.x += self.speed
            if self.rect.x >= 0:
                self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.rect.x > screen_width - 30:
                self.rect.x -= self.speed
            if self.rect.x <= screen_width -30:
                self.rect.x += self.speed
        if keys[pygame.K_UP]:
            if self.rect.y < 0:
                self.rect.y += self.speed
            if self.rect.y >= 0:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            if self.rect.y > screen_height - 30:
                self.rect.y -= self.speed
            if self.rect.y <= screen_height -30:
                self.rect.y += self.speed

        self.attack_range.topleft = (self.rect.x - 40, self.rect.y - 40)

    def attack(self, enemies):
        if not self.attacking and self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = 12
            self.attack_cooldown = self.attack_cooldown_max

            new_enemies = []
            killed = []
            for enemy in enemies:
                if self.attack_range.colliderect(enemy.rect):
                    killed.append(enemy)
                else:
                    new_enemies.append(enemy)
            enemies[:] = new_enemies
            return killed
        return []

    def haste(self):
        self.attack_cooldown_max *= (1/2)
        self.haste_timer += 10 * FPS

    def shield(self):
        self.shield_timer += SHIELD_DURATION

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.haste_timer > 0:
            self.haste_timer -= 1
            if self.haste_timer == 0:
                self.attack_cooldown_max = self.attack_cooldown_base
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.attacking:
            pygame.draw.rect(screen, (255, 255, 255), self.attack_range, 2)
        else:
            pygame.draw.rect(screen, (0,0,0), self.attack_range, 1)
        for l in range(self.lives):
            pygame.draw.rect(screen, (255, 255, 0), (10 + l * 30,10,20,20))
        cell_text = game_font.render(str(self.attack_cooldown), True, WHITE)
        text_rect = (screen_width-100,screen_height-100)
        screen.blit(cell_text, text_rect)


class Enemy:
    def __init__(self):
        self.rect  = pygame.Rect(random.randint(0, screen_width -40), random.randint(0,screen_height-40), 40 ,40)
        self.speed = 2
    
    def move_towards(self, target):
        if self.rect.x < target.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > target.rect.x:
            self.rect.x -= self.speed
        if self.rect.y < target.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > target.rect.y:
            self.rect.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, (0,255,0), self.rect)

class Heal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.duration = 10 * FPS

    def update(self):
        self.duration -= 1

    def expired(self):
        return self.duration <= 0

    def draw(self):
        pygame.draw.rect(screen, (255,105,180), self.rect)

class Haste:
    def __init__ (self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.duration = 10 * FPS

    def update(self):
        self.duration -= 1

    def expired(self):
        return self.duration <= 0

    def draw(self):
        pygame.draw.rect(screen, (105,255,180), self.rect)

class Shield:
    def __init__ (self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.duration = 10 * FPS

    def update(self):
        self.duration -= 1

    def expired(self):
        return self.duration <= 0

    def draw(self):
        pygame.draw.rect(screen, (255,255,25), self.rect)

def main():
    run = True
    player = Player()
    enemy = [Enemy() for _ in range(3)]
    heals = []
    hastes = []
    shields = []
    score = 0

    enemy_spawn_timer = 0
    enemy_spawn_interval = 120
    while run:
        clock.tick(FPS)
        screen.fill((0,0,0))
        score += 1/FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        
        if keys[pygame.K_SPACE]:
            killed = player.attack(enemy)
            score += len(killed) * 10
            for e in killed:
                ran = random.random()
                if len(heals) < MAX_HEAL and ran <= HEAL_DROP_CHANCE:
                    heals.append(Heal(e.rect.x, e.rect.y))
                tmp = HEAL_DROP_CHANCE
                if len(hastes) < MAX_HASTE and tmp < ran <= tmp + HASTE_DROP_CHANCE:
                    hastes.append(Haste(e.rect.x, e.rect.y))
                tmp += HASTE_DROP_CHANCE
                if len(shields) < MAX_SHIELD and tmp < ran <= tmp + SHIELD_DROP_CHANCE:
                    shields.append(Shield(e.rect.x, e.rect.y))

        enemy_spawn_timer += 1
        if enemy_spawn_timer>= enemy_spawn_interval:
            enemy.append(Enemy())
            enemy_spawn_timer = 0

        for e in enemy:
            e.move_towards(player)
        
        for e in enemy:
            if player.rect.colliderect(e.rect) and player.shield_timer == 0:
                player.lives -= 1
                enemy.remove(e)

        for h in heals:
            h.update()
            if h.expired():
                heals.remove(h)
                continue
            if player.rect.colliderect(h.rect) and player.lives < MAX_LIVES:
                player.lives += 1
                heals.remove(h)

        for hs in hastes:
            hs.update()
            if hs.expired():
                hastes.remove(hs)
                continue
            if player.rect.colliderect(hs.rect) and player.haste_timer == 0:
                player.haste()
                hastes.remove(hs)
        for s in shields:
            s.update()
            if s.expired():
                shields.remove(s)
                continue
            if player.rect.colliderect(s.rect) and player.shield_timer == 0:
                player.shield()
                shields.remove(s)

        player.update()
        player.draw()
        
        for e in enemy:
            e.draw()
        for h in heals:
            h.draw()
        for hs in hastes:
            hs.draw()
        for s in shields:
            s.draw()
        if player.lives <= 0:
            pygame.time.delay(2000)
            run = False
        pygame.display.update()
    
    pygame.quit()
    exit()
if __name__ == "__main__":
    main()