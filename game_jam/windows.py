"""Graphical elements that make up the graphical user interface. Should only contain data"""

from events import *
from gui import Window, Button, WIDTH
from values import Defaults

volume = Defaults.volume

menu = Window(caption="JellySmash Menu")
menu.elements = {
    "open": Button("Start", (WIDTH // 2 - 100, 200, 200, 50)),
    "settings": Button("Settings", (WIDTH // 2 - 100, 300, 200, 50), on_click=open_settings),
    "exit": Button("Exit", (WIDTH // 2 - 100, 400, 200, 50), on_click=exit_game),
}

settings = Window(caption="JellySmash Settings")
settings.elements = {
    "increase_sound": Button("->", (WIDTH // 2 + 125, 200, 50, 50,), on_click=increase_volume),
    "decrease_sound": Button("<-", (WIDTH // 2 - 175, 200, 50, 50), on_click=decrease_volume),
    "sound": Button(f"Sound: {Defaults.volume * 100:.0f}", (WIDTH // 2 - 100, 200, 200, 50), on_update=update_volume,
                    on_click=reset_sound),
    "back": Button("Back", (WIDTH // 2 - 100, 400, 200, 50), on_click=to_menu),
}
