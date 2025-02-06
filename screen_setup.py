import pygame
import sys
pygame.font.init()

# Font definition
font = pygame.font.SysFont('Verdana', 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Screen setup
background_image = pygame.image.load("images/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sayo's Pet Game")