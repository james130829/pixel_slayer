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
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class Enemy:
    def __init__(self):
        self.rect  = pygame.Rect(random.randint(0, screen_width -40), random.randint(0,screen_height-40), 40 ,40)
    
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
        
        player.draw()
        
        for e in enemy:
            e.draw()
        
        pygame.display.update()

    pygame.quit()
    exit()
if __name__ == "__main__":
    main()