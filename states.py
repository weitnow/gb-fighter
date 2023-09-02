import pygame
from utils import aseprite





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

class CrouchState(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)

    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('Crouch')

    def render_state(self) -> None:
        super().render_state()
        

    def _exit_state(self) -> None:
        pass

class A_Move_State(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)

    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('A Move')

    def render_state(self) -> None:
        super().render_state()
        

    def _exit_state(self) -> None:
        pass

class B_Move_State(State):
    def __init__(self, actor) -> None:
        super().__init__(actor)

    def _enter_state(self) -> None:
        self.frame_index = 0
        self.animation = aseprite.get_animation('B Move')

    def render_state(self) -> None:
        super().render_state()
        

    def _exit_state(self) -> None:
        pass