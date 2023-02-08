"""The entry point of the game."""
import pygame
from pathlib import Path
from windows import menu
from gameplay import Level
menu.open()
ASSETS = Path(__file__).parent.parent / "assets"
SPRITES = ASSETS / "sprites"
SOUNDS = ASSETS / "sounds"

image = SPRITES / "magentaJar.png"
song = SOUNDS / "ode-to-joy.wav"

