import pygame, sys
import settings.game
from fighter import Fighter
from pygame.math import Vector2
from utils import aseprite


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((settings.game.WINDOW_WIDTH, settings.game.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.game.TITLE)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('./graphics/stage.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5, 96 * 5))

        self.setup()

        #music
        self.music = pygame.mixer.Sound('./music/guile_music.mp3')
        if settings.game.MUSIC:
            self.music.play(loops = -1)

    def setup(self):
        aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)

        self.fighter1 = Fighter(self.screen, Vector2(400, 280))
        self.fighter2 = Fighter(self.screen, Vector2(700, 280))
        self.fighter2.ai = True

    def face_players_each_other(self):
        if self.fighter1.rect.x >= self.fighter2.rect.x:
            self.fighter1.facing = 'left'
            self.fighter2.facing = 'right'
        else:
            self.fighter1.facing = 'right'
            self.fighter2.facing = 'left'  

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.screen.fill((155,188,15))
            self.screen.blit(self.background, (0, 0))

            self.fighter1.update(dt)
            #self.fighter2.update(dt)
            self.face_players_each_other()
 
            pygame.display.update()


        
if __name__ == '__main__':
    main = Main()
    main.run()