import pygame, sys
import settings.window
from text import Text

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.window.WINDOW_WIDTH, settings.window.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.window.TITLE)
        self.clock = pygame.time.Clock()

        self.setup()
        self.text = Text()

        background_width = 256
        background_height = 96

        screen_width = 1280
        screen_height = 720

        zoom_width = int(screen_width // background_width)
        zoom_height = int(screen_height // background_height)


        self.background = pygame.image.load('./graphics/stage.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5, 96 * 5))

    
    def setup(self):
        pass


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((155,188,15))
            self.display_surface.blit(self.background, (0, 0))



            pygame.display.update()

            
        
if __name__ == '__main__':
    main = Main()
    main.run()