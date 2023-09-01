import pygame
from pygame.math import Vector2
from utils import aseprite, joystick
from states import *
import settings

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos: Vector2):
        super().__init__()

        self.get_state = {
            "idle" : IdleState(self),
            "walking" : WalkingState(self),
            "jump" : JumpState(self),
            "crouch" : CrouchState(self),
            "a move" : A_Move_State(self),
            "b move" : B_Move_State(self)
        }

        self.renderstate = self.get_state["idle"]
        self.previous_state = None

        self.surface = pygame_surface

        self.facing = 'left'

        #image setup
        self.animation = aseprite.get_animation('Idle')
        self.image = self.animation[0]
        self.rect = self.image.get_rect(topleft=pos)

        #float based movement
        self.direction = Vector2()
        self.pos = pos
        self.speed = 400
        self.jump_speed = 960
        self.on_floor = True

        self.ai = False

    def change_state(self, new_state: State):
        if new_state != self.renderstate:
            if isinstance(self.renderstate, State):
                self.renderstate._exit_state()
            new_state._enter_state()
            self.previous_state = self.renderstate
            self.renderstate = new_state

    def transition_from_state_to_state(self):
        if self.direction.x != 0 and self.direction.y == 0 and self.renderstate != self.get_state["walking"]:
            self.change_state(self.get_state["walking"])
        if self.direction.x == 0 and self.direction.y == 0 and self.renderstate != self.get_state["idle"]:
            self.change_state(self.get_state["idle"])
        if self.direction.y != 0 and self.renderstate != self.get_state["jump"]:
            self.change_state(self.get_state["jump"])

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

        if (keys[pygame.K_w] or joystick.dpad_up) and self.on_floor:
            self.direction.y = -self.jump_speed
            self.on_floor = False

        if joystick.a_pressed:
            self.change_state(self.get_state['a move'])

        if joystick.b_pressed:
            self.change_state(self.get_state['b move'])

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
        self.transition_from_state_to_state()
        self.renderstate.update_state(dt)
        self.renderstate.render_state()