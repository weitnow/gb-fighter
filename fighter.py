import pygame
from pygame.math import Vector2
from utils import aseprite

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos: Vector2):
        super().__init__()

        self.surface = pygame_surface

        #graphics setup
        self.idle = aseprite.get_animation('Idle')
        self.frame_index = 0
        self.status = 'left'

        #image setup
        self.image = self.idle[self.frame_index]

        #float based movement
        self.direction = Vector2()
        self.pos = pos
        self.speed = 400
        self.jump_speed = 500

        self.ai = False
        
    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.idle):
            self.frame_index = 0

        self.image = self.idle[int(self.frame_index)]

        if self.status == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        
    def draw(self):
        self.surface.blit(self.image, (self.pos.x, self.pos.y))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_w] and self.on_floor:
            self.direction.y = -self.jump_speed

    def move(self, dt):
        if self.ai:
            return
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.draw()



