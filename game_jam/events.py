"""Events that are triggered for a specific object every frame."""

import sys

from gui import Window
from values import Defaults

import pygame


def exit_game(window: Window) -> None:
    """Closes the game and thanks the player."""

    print("Thanks for playing!")
    pygame.quit()
    sys.exit()


def open_settings(window: Window):
    """Close the current window and open the settings menu."""

    window.close()

    from windows import settings

    settings.open()


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

    from windows import menu

    menu.open()


def update_volume(window: Window):
    """Updates the text of the message button."""

    window.get_element("sound").message = f"Sound: {Defaults.volume * 100:.0f}"
