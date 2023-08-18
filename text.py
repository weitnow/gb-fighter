import pygame
import settings.color

class Text:
    def __init__(self):
        font = pygame.font.Font('freesansbold.ttf', 32)

        text = font.render('Drucker1', True, settings.color.GREEN, settings.color.BLUE)

        textRect = text.get_rect()

        textRect.center = (100, 100)