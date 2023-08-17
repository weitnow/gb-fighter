import pygame, sys
import settings

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((249, 131, 103))

            pygame.display.update()

            
        
if __name__ == '__main__':
    main = Main()
    main.run()