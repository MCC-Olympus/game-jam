"""Values that don't change and are used by multiple files"""

from pathlib import Path

import pygame

NAME = "JellySmash"

ASSETS = Path(__file__).parent.parent / "assets"
SPRITES = ASSETS / "sprites"
SOUNDS = ASSETS / "sounds"

pygame.display.init()
WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)

FPS = 60
FRAMES_PER_ANIMATION = 5

# Type hints
Coordinate = tuple[int, int]
RGB = tuple[int, int, int]
Rect = tuple[int, int, int, int]
