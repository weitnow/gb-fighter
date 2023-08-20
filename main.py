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

        
        self.text = Text()

        background_width = 256
        background_height = 96

        screen_width = 1280
        screen_height = 720

        zoom_width = int(screen_width // background_width)
        zoom_height = int(screen_height // background_height)


        #######################################################
        self.last_update = pygame.time.get_ticks()
        self.update_every_ms = 100
        self.index = 0

        #######################################################

        self.background = pygame.image.load('./graphics/stage.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5, 96 * 5))


        self.setup()


    
    def setup(self):
        self.animlist_pygame_surfaces, self.animlist = aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)
        aseprite.store_animation_names()

        self.fighter = Fighter(self.display_surface, (500, 280))




   

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.display_surface.fill((155,188,15))
            self.display_surface.blit(self.background, (0, 0))
            self.display_surface.blit(self.animlist_pygame_surfaces[self.index], (200, 280))
            self.update_index()

            self.fighter.update(dt)



            pygame.display.update()

    def update_index(self):
        if self.last_update + self.update_every_ms < pygame.time.get_ticks():
            self.index += 1
            self.last_update = pygame.time.get_ticks()
            if self.index >= len(self.animlist_pygame_surfaces):
                self.index = 0




        
if __name__ == '__main__':
    main = Main()
    main.run()