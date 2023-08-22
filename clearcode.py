import pygame, sys

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


class Player(object):
    
    def __init__(self):
        self.player = pygame.rect.Rect((300, 400, 50, 50))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip(x_speed, y_speed)

    def change_color(self, color):
        self.color = color

    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800))
second_surface = pygame.Surface([100, 200])
second_surface.fill((0, 0, 255))
second_surface_rect = second_surface.get_rect()

player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.JOYBUTTONDOWN:
            if pygame.joystick.Joystick(0).get_button(0):
                player.change_color("blue")
            elif pygame.joystick.Joystick(0).get_button(1):
                player.change_color("red")
            elif pygame.joystick.Joystick(0).get_button(2):
                player.change_color("yellow")
            elif pygame.joystick.Joystick(0).get_button(3):
                player.change_color("green")

        if event.type == pygame.JOYHATMOTION:
            print(pygame.joystick.Joystick(0).get_numhats)
    

        
    screen.fill((0, 0, 0))

    screen.blit(second_surface, second_surface_rect)
    player.draw(screen)
    pygame.display.update()

    clock.tick(60)