"""The entry point of the game."""
from windows import menu
import pygame
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
print(WIDTH)
print(HEIGHT)
menu.open()
