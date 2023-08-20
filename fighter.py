import pygame
from utils import aseprite

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos):
        super().__init__()

        self.surface = pygame_surface

        #graphics setup
        self.idle = aseprite.get_animation('Idle')
        self.frame_index = 0
        self.status = 'right'

        #image setup
        self.image = self.idle[self.frame_index]

        #float based movement
        self.pos = pos
        
    def update(self, dt):
        self.animate(dt)
        self.draw()

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.idle):
            self.frame_index = 0

        self.image = self.idle[int(self.frame_index)]

    def draw(self):
        self.surface.blit(self.image, self.pos)




