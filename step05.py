import pygame
import random

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 20, 40, 40)
        self.speed = 5
        self.lives = 3

        self.attack_range = pygame.Rect(self.rect.x -30, self.rect.y -30, 100, 100)
        self.attacking = False
        self.attack_timer = 0

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

        self.attack_range.topleft = (self.rect.x - 30, self.rect.y - 30)

    def attack(self, enemies):
        if not self.attacking:
            self.attacking = True
            self.attack_timer = 12

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

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.attacking:
            pygame.draw.rect(screen, (255, 255, 255), self.attack_range, 2)
        else:
            pygame.draw.rect(screen, (0,0,0), self.attack_range, 1)
        for l in range(self.lives):
            pygame.draw.rect(screen, (255, 255, 0), (10 + l * 30,10,20,20))

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