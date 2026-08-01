import pygame
import random

pygame.init()

game_font = pygame.font.Font(None, 120)
WHITE = (255,255,255)
screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 20, 40, 40)
        self.speed = 5
        self.lives = 3

        self.attack_range = pygame.Rect(self.rect.x -40, self.rect.y -40, 120, 120)
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0

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
            self.attack_cooldown = 300

            new_enemies = []
            for enemy in enemies:
                if not self.attack_range.colliderect(enemy.rect):
                    new_enemies.append(enemy)
            enemies[:] = new_enemies

    def update(self):
        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

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

def main():
    run = True
    player = Player()
    enemy = [Enemy() for _ in range(3)]

    enemy_spawn_timer = 0
    enemy_spawn_interval = 120
    while run:
        clock.tick(FPS)
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        if keys[pygame.K_SPACE]:
            player.attack(enemy)

        enemy_spawn_timer += 1
        if enemy_spawn_timer>= enemy_spawn_interval:
            enemy.append(Enemy())
            enemy_spawn_timer = 0

        for e in enemy:
            e.move_towards(player)
        
        for e in enemy:
            if player.rect.colliderect(e.rect):
                player.lives -= 1
                enemy.remove(e)

        player.update()
        player.draw()
        
        for e in enemy:
            e.draw()
        if player.lives <= 0:
            pygame.time.delay(2000)
            run = False
        pygame.display.update()
    
    pygame.quit()
    exit()
if __name__ == "__main__":
    main()