"""Events that are triggered for a specific object every frame."""

from gameplay import Level
from gui import *
from values import Defaults
from constants import *
import pygame


song1 = SOUNDS / "ode-to-joy.wav"
song2 = SOUNDS / "rushE.wav"
song3 = SOUNDS / "gamemusic-6082.wav"


def exit_game(window: Window) -> None:
    """Closes the game and thanks the player."""

    print("Thanks for playing!")
    pygame.quit()
    sys.exit()


def open_settings(window: Window):
    """Close the current window and open the settings menu."""

    window.close()
    pygame.time.wait(200)

    from windows import settings

    settings.open()


def open_level_select(window: Window):
    window.close()
    pygame.time.wait(200)

    from windows import level_select

    level_select.open()


def increase_volume(window: Window):
    """Increase the volume by 0.1, if possible."""

    Defaults.volume = min(Defaults.volume + 0.1, 1)


def decrease_volume(window: Window):
    """Decrease the volume by 0.1, if possible."""

    Defaults.volume = max(Defaults.volume - 0.1, 0)


def reset_sound(window: Window):
    """Either mutes the volume or sets it to halfway, depending on how it currently is."""

    if Defaults.volume == 0:
        Defaults.volume = 0.5
    else:
        Defaults.volume = 0


def to_menu(window: Window):
    """Close the current window and open the main menu."""

    window.close()
    pygame.time.wait(200)

    from windows import menu

    menu.open()


def update_volume(window: Window):
    """Updates the text of the message button."""

    window.get_element("sound").message = f"Sound: {Defaults.volume * 100:.0f}"


def lvl_one_run(window: Window):
    game = Level("Game Jam Level 1", song1)
    game.open()


def lvl_two_run(window: Window):
    game = Level("Game Jam Level 2", song2, speed=6)
    game.open()


def lvl_three_run(window: Window):
    game = Level("Game Jam Level 3", song3, speed=7)
    game.open()


def do_nothing(window: Window):
    pass
