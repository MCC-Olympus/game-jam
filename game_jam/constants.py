"""Values that don't change and are used by multiple files"""

from pathlib import Path
from typing import Callable

import pygame

NAME = "JellySmash"

GAME_JAM = Path(__file__).parent
ROOT = GAME_JAM.parent
ASSETS = ROOT / "assets"
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
Function = Callable[[], None]
