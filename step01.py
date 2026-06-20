import pygame

pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
FPS = 60

class Player:
    def __init__(self):
        self.rect = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 20, 40, 40)
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

def main():
    run = True
    player = Player()

    while run:
        clock.tick(FPS)
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        player.draw()
        
        pygame.display.update()

    pygame.quit()
    exit()
if __name__ == "__main__":
    main()