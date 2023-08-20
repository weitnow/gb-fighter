import pygame, sys
import settings.window
from text import Text
from fighter import Fighter
from pygame.math import Vector2
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

        #music
        self.music = pygame.mixer.Sound('./music/guile_music.mp3')
        self.music.play(loops = -1)

    def setup(self):
        aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)

        self.fighter1 = Fighter(self.display_surface, Vector2(400, 280))
        self.fighter2 = Fighter(self.display_surface, Vector2(700, 280))
        self.fighter2.ai = True

    
    def flip_players_towards_each_other(self):
        if self.fighter1.pos.x >= self.fighter2.pos.x:
            self.fighter1.status = 'left'
            self.fighter2.status = 'right'
        else:
            self.fighter1.status = 'right'
            self.fighter2.status = 'left'


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
            self.flip_players_towards_each_other()

            pygame.display.update()


        
if __name__ == '__main__':
    main = Main()
    main.run()