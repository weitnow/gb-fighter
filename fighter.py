import pygame
from pygame.math import Vector2
from utils import aseprite, joystick
import settings
class State():
    def __init__(self, actor):
        self.actor = actor
        self.frame_index = 0
        self.animation = aseprite.get_animation('Idle')
        self.image = self.animation[self.frame_index]

    def update_state(self, dt) -> None:
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.animation):
            self.frame_index = 0

    def _enter_state(self) -> None:
        print("Enter State")

    def render_state(self) -> None:
        self.image = self.animation[int(self.frame_index)]

        if self.actor.facing == 'left':
            self.image = pygame.transform.flip(self.image, True, False)

        self.actor.surface.blit(self.image, self.actor.rect)

    def _exit_state(self) -> None:
        print("Exiting State")

class IdleState(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)
        
    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('Idle')
        

    def render_state(self) -> None:
        super().render_state()
      
    def _exit_state(self) -> None:
        print("Exiting IdleState")

class WalkingState(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)

    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('Walking')

    def render_state(self) -> None:
        super().render_state()

    def _exit_state(self) -> None:
        print("Exiting WalkingState")

class JumpState(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)

    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('Jump')

    def render_state(self) -> None:
        super().render_state()
        

    def _exit_state(self) -> None:
        print("Exiting JumpState")


##########################################################################

class Fighter(pygame.sprite.Sprite):
    def __init__(self, pygame_surface, pos: Vector2):
        super().__init__()

        self.states = {
            "idle" : IdleState(self),
            "walking" : WalkingState(self),
            "jump" : JumpState(self)
        }

        self.state = self.states["idle"]
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
        if new_state != self.state:
            if isinstance(self.state, State):
                self.state._exit_state()
            new_state._enter_state()
            self.previous_state = self.state
            self.state = new_state

    def transition_from_state_to_state(self):
        if self.direction.x != 0 and self.direction.y == 0 and self.state != self.states["walking"]:
            self.change_state(self.states["walking"])
        if self.direction.x == 0 and self.direction.y == 0 and self.state != self.states["idle"]:
            self.change_state(self.states["idle"])
        if self.direction.y != 0 and self.state != self.states["jump"]:
            self.change_state(self.states["jump"])

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

        if joystick.a_pressed and self.on_floor:
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
        self.state.update_state(dt)
        self.state.render_state()