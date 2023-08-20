import pygame, sys
import settings.window
from text import Text
from fighter import Fighter
from utils import aseprite

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.window.WINDOW_WIDTH, settings.window.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.window.TITLE)
        self.clock = pygame.time.Clock()

        background_width = 256
        background_height = 96

        screen_width = 1280
        screen_height = 720

        self.background = pygame.image.load('./graphics/stage.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5, 96 * 5))


        self.setup()
    
    def setup(self):
        aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)

        self.fighter1 = Fighter(self.display_surface, (400, 280))
        self.fighter1.status = 'right'
        self.fighter1.idle = aseprite.get_animation('B Move')
        self.fighter2 = Fighter(self.display_surface, (700, 280))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((155,188,15))
            self.display_surface.blit(self.background, (0, 0))

            self.fighter1.update(dt)
            self.fighter2.update(dt)

            pygame.display.update()


        
if __name__ == '__main__':
    main = Main()
    main.run()