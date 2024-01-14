import pygame

ASSETS_BASE_PATH = 'assets/'

def render_text (text, font, color, size):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, color)

    return text

def load_image (path):
    path = ASSETS_BASE_PATH + path

    return pygame.image.load(path)
