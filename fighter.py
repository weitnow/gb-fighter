import pygame
from pygame.math import Vector2
from utils import aseprite, joystick
import settings

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos: Vector2):
        super().__init__()

        self.surface = pygame_surface

        #graphics setup
        self.animation = aseprite.get_animation('Idle')
        self.frame_index = 0
        self.facing = 'left'
        self.state = 'Idle'

        #image setup
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        #float based movement
        self.direction = Vector2()
        self.pos = pos
        self.speed = 400
        self.jump_speed = 960
        self.on_floor = True



        self.ai = False
        
    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animation):
            self.frame_index = 0

        self.image = self.animation[int(self.frame_index)]

        if self.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        

        #walk
        if self.direction.x != 0 and self.direction.y == 0 and self.state != "Walking":
            self.frame_index = 0
            self.animation = aseprite.get_animation('Walking')
            self.state = "Walking"
        if self.direction.x == 0 and self.direction.y == 0 and self.state != "Idle":
            self.frame_index = 0
            self.animation = aseprite.get_animation('Idle')
            self.state = "Idle"
        if self.direction.y != 0 and self.state != "Jump":
            self.frame_index = 0
            self.animation = aseprite.get_animation('Jump')
            self.state = "Jump"



    def draw(self):
        self.surface.blit(self.image, self.rect)

    def input(self):

        if self.ai:
            return
        


        joystick.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or joystick.dpad_right:
            self.direction.x = 1
        elif keys[pygame.K_a] or joystick.dpad_left:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_w] or joystick.dpad_up and self.on_floor:
            self.direction.y = -self.jump_speed
            self.on_floor = False

    def move(self, dt):
        if self.ai:
            return
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        
        # vertical movement
        self.pos.y += self.direction.y * dt
        self.rect.y = round(self.pos.y)

        # ensure player stays on screen
        if self.rect.left < -20:
            self.rect.left = -20
            self.pos.x = self.rect.left
        elif self.rect.right > settings.game.WINDOW_WIDTH + 20:
            self.rect.right = settings.game.WINDOW_WIDTH + 20
            self.pos.x = self.rect.left


    def apply_gravity(self, dt):
        if self.pos.y < 280:
            self.direction.y += settings.game.GRAVITY * dt
        if self.pos.y > 280:
            self.pos.y = 280
            self.direction.y = 0
            self.on_floor = True
       


    def update(self, dt):
        self.input()
        self.move(dt)
        self.apply_gravity(dt)
        self.animate(dt)
        self.draw()



