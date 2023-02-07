"""The entry point of the game."""

from pathlib import Path

from gameplay import Level

ASSETS = Path(__file__).parent.parent / "assets"
SPRITES = ASSETS / "sprites"
SOUNDS = ASSETS / "sounds"

image = SPRITES / "magentaJar.png"
song = SOUNDS / "ode-to-joy.wav"

game = Level("Game Jam", song)

game.open()
