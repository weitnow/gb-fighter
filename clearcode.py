import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800, 800))
second_surface = pygame.Surface([100, 200])
second_surface.fill((0, 0, 255))
second_surface_rect = second_surface.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill((255, 255, 255))

    screen.blit(second_surface, second_surface_rect)
    second_surface_rect.right += 5
    pygame.display.flip()

    clock.tick(4)