import pygame
import settings.color

def draw_text(text: str, x: int, y: int, screen: pygame.surface, font: str = 'freesansbold.ttf', size: int = 32, text_color: tuple = (255, 255, 255), bg_color: tuple = (0, 0, 0)):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, text_color, bg_color)
    textRect = text.get_rect()
    textRect = (x, y)
    screen.blit(text, textRect)
    