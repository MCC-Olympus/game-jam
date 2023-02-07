"""The entry point of the game."""

from pathlib import Path

from gameplay import Level
from gui import Button


def smash_jar(level: Level):
    del level.jars[0]
    print("smashing jar...")


image = Path("../assets/sprites/magentaJar.png")
song = Path("../assets/sounds/ode-to-joy.wav")

game = Level("Game Jam", song)
game.jars = [Button(image, (500, 200), on_click=smash_jar)]

game.open()
