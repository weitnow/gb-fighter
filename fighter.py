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
            "a move" : A_Move_State(self),  #kicking
            "b move" : B_Move_State(self)   #punching
        }
        self.renderstate = self.get_state["idle"]
        
        self.state = "idle"
        
        self.surface = pygame_surface

        self.facing = 'left'
        self.input_block = False
        self.transition_block = False

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

        self.new_timer = None
        self.call_back = None
        self.ms = None

    def change_attr(self, attr: str, val):
        '''takes an attribute-name and a value and sets the attribute to this val \n
        for example change_attr(transition_block, True)'''
        setattr(self, attr, val)

    def change_state(self, new_state: State):
        if new_state != self.renderstate:
            if isinstance(self.renderstate, State):
                self.renderstate._exit_state()
            new_state._enter_state()
            self.renderstate = new_state

    def transition_from_state_to_state(self):
        if self.transition_block:
            return
        
        if self.direction.x != 0 and self.direction.y == 0 and self.state != "walking":
            self.state = "walking"
        if self.direction.x == 0 and self.direction.y == 0 and self.state != "idle":
            self.state = "idle"
        if self.direction.y != 0 and self.state != "jump":
            self.state = "jump"

    def update_state(self, dt):
        self.change_state(self.get_state[self.state])
        self.transition_from_state_to_state()
        self.renderstate.update_state(dt)
        self.renderstate.render_state()

    def punch(self):
        if self.state != "jump":
            self.state = "b move" #punch

    def kick(self):
        if self.state != "jump":
            self.state = "a move" #kick

    def input(self):
        if self.ai or self.input_block:
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
            self.kick()
            
        if joystick.b_pressed:
            self.activate_timer_callback(self.kick, 1000)
            self.punch()

        if joystick.x_pressed:
            self.change_attr("transition_block", True)

        if joystick.y_pressed:
            pass

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

    
    def activate_timer_callback(self, call_back, ms):
        if self.new_timer is None:
            self.new_timer = pygame.time.get_ticks()
            self.call_back = call_back
            self.ms = ms
            

    def update_timer(self):
        if self.new_timer is not None:
            if self.new_timer + self.ms <= pygame.time.get_ticks():
                self.new_timer = None
                self.ms = None
                print(self.call_back)
                self.call_back()
                eval('self.change_attr("transition_block", True)')

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
        self.update_state(dt)
        self.update_timer()