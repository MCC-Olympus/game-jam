"""Entry point of the game."""

import asyncio
import sys

import pygame

from game_jam.constants import WIDTH, HEIGHT, FPS, SPRITES, NAME, SOUNDS
from game_jam.events import (
    open_window,
    exit_game,
    get_value,
    increase_volume,
    decrease_volume,
    update_volume,
    reset_volume,
)
from game_jam.gameplay import Level
from game_jam.gui import Window, Button, TextButton


class Game:
    """The grouping class for specifying the windows and the running loop."""

    def __init__(self):
        self.windows = {}
        self.running_window = None
        self._clock = pygame.time.Clock()

        pygame.init()

    async def run(self):
        while True:
            window = self.get_window(self.running_window)

            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            window.on_update()
            window.update_elements(self)
            window.display_elements()

            await asyncio.sleep(0)

    def get_window(self, name) -> Window:
        """
        Retrieve the window object with the given name.

        :param name: The name of the window.
        :returns: The desired Window object.
        """
        return self.windows.get(name)

    def open(self, name) -> None:
        """
        Sets a new window as the window to be displayed and updated.

        :param name: The name of the window to display.
        """

        self.running_window = name
        pygame.display.set_caption(f"{NAME} | {name}")

        window = self.get_window(name)
        if isinstance(window, Level):
            window.load()

    @staticmethod
    def exit() -> None:
        """
        End the game.
        """

        print("Thanks for playing!")
        pygame.quit()
        sys.exit()


my_game = Game()

# The entire gui is defined in this dictionary. Each key is the name of the element, and the
# value is an instance of the Window class (or Level, since it inherits from Window). Each Window
# is made up of Elements, defined as another dictionary.
my_game.windows = {
    "Menu": Window(
        SPRITES / "sbg.png",
        {
            "open": Button(
                SPRITES / "startButton.png",
                (WIDTH // 2 - 100, 100),
                scale=2,
                on_click=open_window(my_game, "Level Selector"),
            ),
            "settings": Button(
                SPRITES / "settingsButton.png",
                (WIDTH // 2 - 150, 300),
                scale=2,
                on_click=open_window(my_game, "Settings"),
            ),
            "exit": Button(
                SPRITES / "exitButton.png",
                (WIDTH // 2 - 50, 500),
                scale=2,
                on_click=exit_game(my_game),
            ),
        },
    ),
    "Level Selector": Window(
        SPRITES / "bg.png",
        {
            "Level One": Button(
                SPRITES / "lvlOneButton.png",
                (WIDTH // 5 - 100, HEIGHT // 4),
                border_radius=0,
                scale=3,
                on_click=open_window(my_game, "Level One"),
            ),
            "Level Two": Button(
                SPRITES / "lvlTwoButton.png",
                (2 * WIDTH // 5 - 100, HEIGHT // 4),
                border_radius=0,
                scale=3,
                on_click=open_window(my_game, "Level Two"),
            ),
            "Level Three": Button(
                SPRITES / "lvlThreeButton.png",
                (3 * WIDTH // 5 - 100, HEIGHT // 4),
                border_radius=0,
                scale=3,
                on_click=open_window(my_game, "Level Three"),
            ),
            "Endless Mode": Button(
                SPRITES / "endlessButton.png",
                (4 * WIDTH // 5 - 100, HEIGHT // 4),
                scale=3,
                on_click=open_window(my_game, "Menu"),
            ),
            "Back": Button(
                SPRITES / "backButton.png",
                (WIDTH // 2 - 100, 2 * HEIGHT // 4),
                scale=3,
                on_click=open_window(my_game, "Menu"),
            ),
        },
    ),
    "Settings": Window(
        SPRITES / "bg.png",
        {
            "Increase song volume": TextButton(
                ">",
                (
                    WIDTH // 2 + 125,
                    200,
                    50,
                    50,
                ),
                on_click=increase_volume("Song"),
            ),
            "Decrease song volume": TextButton(
                "<",
                (WIDTH // 2 - 175, 200, 50, 50),
                on_click=decrease_volume("Song"),
            ),
            "Increase effect volume": TextButton(
                ">",
                (
                    WIDTH // 2 + 125,
                    300,
                    50,
                    50,
                ),
                on_click=increase_volume("Effects"),
            ),
            "Decrease effect volume": TextButton(
                "<",
                (WIDTH // 2 - 175, 300, 50, 50),
                on_click=decrease_volume("Effects"),
            ),
            "Song Volume": TextButton(
                f"Music: {get_value('Song Volume') * 100:.0f}",
                (WIDTH // 2 - 100, 200, 200, 50),
                on_update=update_volume(my_game, "Settings", "Song"),
                on_click=reset_volume("Song"),
            ),
            "Effects Volume": TextButton(
                f"Effects: {get_value('Song Volume') * 100:.0f}",
                (WIDTH // 2 - 100, 300, 200, 50),
                on_update=update_volume(my_game, "Settings", "Effects"),
                on_click=reset_volume("Effects"),
            ),
            "Back": TextButton(
                "Back",
                (WIDTH // 2 - 100, 400, 200, 50),
                on_click=open_window(my_game, "Menu"),
            ),
        },
    ),
    "Level One": Level(
        my_game,
        SOUNDS / "ode-to-joy.ogg",
    ),
    "Level Two": Level(
        my_game,
        SOUNDS / "rushE.ogg",
        speed=6,
    ),
    "Level Three": Level(
        my_game,
        SOUNDS / "gamemusic-6082.ogg",
        speed=7,
    ),
    "Game Over": Window(
        SPRITES / "bg.png",
        {
            "message": TextButton(
                message="Congratulations, you won!",
                position=(
                    WIDTH // 2 - 250,
                    HEIGHT // 6,
                    500,
                    100,
                ),
                border_radius=5,
                font_size=75,
            ),
            "Score": TextButton(
                message="0",
                position=(WIDTH // 2 - 100, 2 * HEIGHT // 6, 200, 50),
            ),
            "Back": Button(
                SPRITES / "exitButton.png",
                (WIDTH // 2 - 100, 4 * HEIGHT // 6),
                scale=3,
                on_click=open_window(my_game, "Level Selector"),
            ),
        },
    ),
}


def main():
    my_game.running_window = "Menu"
    asyncio.run(my_game.run())


if __name__ == "__main__":
    main()
