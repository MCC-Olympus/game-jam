"""Classes and elements that will appear during the gameplay itself."""

import asyncio
import random
from time import perf_counter

import pygame

from . import audio_processing
from .constants import WIDTH, HEIGHT, SOUNDS, SPRITES, SCREEN
from .events import get_value, toggle_paused, update_scoreboard, update_jar, smash_jar
from .gui import Window, Button, get_sprite_height, Text


class Level(Window):
    """The class for making individual levels."""

    def __init__(self, game, song, speed=5):
        """
        :param game: The Game object that this level belongs to.
        :param song: The path to the song that should play in the background.
        :param speed: How many pixels per second each jar should fall at.
        """

        super().__init__(None, None)
        self.game = game
        self.song = song
        self.speed = speed

        self.score = None
        self.running = None
        self._last_click = None
        self._task = None
        self.timestamps = None

        self.smash_sound = SOUNDS / "smashing_glass.ogg"

        self.elements = {
            "Pause Button": Button(
                SPRITES / "pauseButton.png",
                (1080 * WIDTH // 1336, 598 * HEIGHT // 768),
                scale=2.5,
                on_click=toggle_paused(self),
            ),
            "Lives": [],
            "Jars": [],
            "Score board": Text(
                message=str(self.score),
                position=(
                    997 * WIDTH // 1366,
                    201 * HEIGHT // 768,
                    355 * WIDTH // 1366,
                    100 * HEIGHT // 768,
                ),
                font_size=75,
                on_update=update_scoreboard(self),
            ),
            "Belt One": Button(
                SPRITES / "belt.png",
                (29 * WIDTH // 103, 0),
                0,
                scale=(HEIGHT / get_sprite_height("belt.png")),
            ),
            "Belt Two": Button(
                SPRITES / "belt.png",
                (38 * WIDTH // 103, 0),
                0,
                scale=(HEIGHT / get_sprite_height("belt.png")),
            ),
            "Belt Three": Button(
                SPRITES / "belt.png",
                (47 * WIDTH // 103, 0),
                0,
                scale=(HEIGHT / get_sprite_height("belt.png")),
            ),
            "Belt Four": Button(
                SPRITES / "belt.png",
                (56 * WIDTH // 103, 0),
                0,
                scale=(HEIGHT / get_sprite_height("belt.png")),
            ),
            "Belt Five": Button(
                SPRITES / "belt.png",
                (65 * WIDTH // 103, 0),
                0,
                scale=(HEIGHT / get_sprite_height("belt.png")),
            ),
        }

    def load(self) -> None:
        """Loads in a Level. Resets old progress, if there is any."""

        self.score = 0
        self.running = True
        self._last_click = None

        self.elements["Jars"] = []
        self.elements["Lives"] = [
            Button(
                SPRITES / "redHeart.png",
                (38 * WIDTH // 1336, 65 * HEIGHT // 768),
                scale=3,
            ),
            Button(
                SPRITES / "redHeart.png",
                (143 * WIDTH // 1336, 65 * HEIGHT // 768),
                scale=3,
            ),
            Button(
                SPRITES / "redHeart.png",
                (250 * WIDTH // 1336, 65 * HEIGHT // 768),
                scale=3,
            ),
        ]

        self.timestamps = audio_processing.get_each_note(self.song)

        pygame.mixer.init()
        pygame.mixer.music.load(self.song)

        volume = get_value("Song Volume")
        pygame.mixer.music.set_volume(volume)

        pygame.mixer.music.play()
        self._task = asyncio.create_task(self.spawn_jars())

    def close(self) -> None:
        """Exit the game onto the game over screen."""

        pygame.mixer.music.stop()
        self._task = None
        self.running = False
        self.game.open("Game Over")

    def lose_life(self) -> None:
        """Remove a heart anytime a jar is lost"""

        lives: list = self.elements.get("Lives")
        if len(lives) > 1:
            lives.pop()
        else:
            message = self.game.get_window("Game Over").get_element("message")
            message.message = "You lose!"
            score = self.game.get_window("Game Over").get_element("Score")
            score.message = self.score

            self.close()

    def update_elements(self, game) -> None:
        """Updates each element every frame."""

        for name, element in self.elements.items():
            if name == "Lives":
                continue
            if name == "Jars":
                continue
            element.on_update()
            if element.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    element.on_click()
                    self._last_click = perf_counter()

        if not self.running:
            return

        jars: list = self.elements.get("Jars")
        for jar in jars:
            jar.on_update()
            if jar.is_pressed:
                jar.on_click()

    def display_elements(self):
        """Display each element every frame."""

        SCREEN.blit(self._background, (0, 0))

        for element in (
            [
                element
                for name, element in self.elements.items()
                if name not in ("Lives", "Jars")
            ]
            + self.elements.get("Lives")
            + self.elements.get("Jars")
        ):
            element.show()

        pygame.display.update()

    async def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""

        jars: list = self.elements.get("Jars")

        while True:
            if self.running:
                n = 3
                filename = random.choices(
                    # Each color is n times more likely than a pickle
                    ("pickle", "red", "purple", "magenta"),
                    (1, n, n, n),
                )[0]
                jar = Button(
                    SPRITES / f"{filename}Jar.png",
                    ((30 + (random.randint(0, 4) * 9)) * WIDTH // 103, 0),
                )

                jar.on_update = update_jar(self, jar, self.speed)
                jar.on_click = smash_jar(self, jar)
                jars.append(jar)

                notes = len(self.timestamps)
                sleep_time = 0
                if notes >= 2:
                    sleep_time = self.timestamps[1] - self.timestamps[0]
                elif notes == 1:
                    sleep_time = self.timestamps[0]
                else:
                    self.close()
                await asyncio.sleep(sleep_time)
                self.timestamps.pop()
            else:
                await asyncio.sleep(0)
