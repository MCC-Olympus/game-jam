"""The entry point of the game."""

from pathlib import Path

from gameplay import Level
from gui import Button


def smash_jar(level: Level):
    del level.jars[0]
    print("smashing jar...")


ASSETS = Path(__file__).parent.parent / "assets"
SPRITES = ASSETS / "sprites"
SOUNDS = ASSETS / "sounds"

image = SPRITES / "magentaJar.png"
song = SOUNDS / "ode-to-joy.wav"

game = Level("Game Jam", song)
game.jars = [Button(image, (500, 200), on_click=smash_jar)]

game.open()
