import pygame, sys
import settings.game
from pygame.math import Vector2
from utils import aseprite

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos: Vector2):
        super().__init__()

        self.surface = pygame_surface

        #image setup
        self.pos = pos
        self.animation = aseprite.get_animation('Idle')
        self.image = self.animation[2]
        self.rect = self.image.get_rect(topleft=pos)

        self.access_pixel_data()


    def access_pixel_data(self):
        pixel_array = pygame.surfarray.array3d(self.image)
        print(pixel_array)
        
        # Find rectangle coordinates
        rectangle_coordinates = []
        for y in range(self.image.get_height()):
            for x in range(self.image.get_width()):
                # Check if the pixel is not fully transparent
                if pixel_array[x, y, 2] > 0:
                    rectangle_coordinates.append((x, y))

        # Get the minimum and maximum x and y coordinates
        min_x = min(x for x, y in rectangle_coordinates)
        max_x = max(x for x, y in rectangle_coordinates)
        min_y = min(y for x, y in rectangle_coordinates)
        max_y = max(y for x, y in rectangle_coordinates)

        # Calculate width and height of the rectangle
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Create a pygame.Rect object
        rectangle_rect = pygame.Rect(min_x, min_y, width, height)

        print("Rectangle Coordinates:", rectangle_coordinates)
        print("Rectangle Rect:", rectangle_rect)

        self.hitbox_rect = rectangle_rect
       

class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((settings.game.WINDOW_WIDTH, settings.game.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.game.TITLE)
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('./graphics/stage.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5, 96 * 5))

        self.setup()

    def setup(self):
        #aseprite.anim_import(path_to_jsonfile='./graphics/gbFighter.json', path_to_pngfile='./graphics/gbFighter.png', zoomfactor=6)
        aseprite.anim_import(path_to_jsonfile='./graphics/hitboxes/gbFighterHitBox.json', path_to_pngfile='./graphics/hitboxes/gbFighterHitBox.png', zoomfactor=6)
        self.hitbox = Hitbox(self.screen, (400, 280))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.screen.fill((155,188,15))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.hitbox.image, self.hitbox.rect)

            #draw rect
            pygame.draw.rect(self.screen, (255, 0, 0), self.hitbox.hitbox_rect)

            pygame.display.update()


        
if __name__ == '__main__':
    
    main = Main()
    main.run()