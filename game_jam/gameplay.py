"""Classes and elements that will appear during the gameplay itself."""
import asyncio
import random
import threading
import time
from time import perf_counter

from . import audio_processing
from . import gui
from .constants import *
from .events import get_value, open_window
from .gui import Button, get_sprite_height


class Level(gui.Window):
    """The class for making individual levels."""

    def __init__(self, game, song, speed=5):
        super().__init__(None, None)
        self.game = game
        self.song = song
        self.task = None
        self.speed = speed

        self.jars: list[gui.Button] = []
        self.timestamps = list(audio_processing.get_each_note(song))
        self.smash_sound = SOUNDS / "smashing_glass.ogg"
        self.start = time.perf_counter()
        self.score = 0
        self.paused = False
        self.running = True
        self._last_click = None
        self.pauseButton = gui.Button(
            SPRITES / "pauseButton.png",
            (1080 * WIDTH // 1336, 598 * HEIGHT // 768),
            scale=2.5,
        )
        self.elements = {
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
            "Lives": [
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
            ],
        }

        self.score_board = gui.Text(
            message=str(self.score),
            position=(
                997 * WIDTH // 1366,
                201 * HEIGHT // 768,
                355 * WIDTH // 1366,
                100 * HEIGHT // 768,
            ),
            border_radius=0,
            font_size=75,
        )
        self._thread = threading.Thread(target=self.spawn_jars)

    def load(self):
        self.__init__(self.game, self.song, self.speed)
        pygame.mixer.init()
        pygame.mixer.music.load(self.song)

        volume = get_value("Song Volume")
        pygame.mixer.music.set_volume(volume)

        pygame.mixer.music.play()
        self.running = True
        self.task = asyncio.create_task(self.spawn_jars())

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        time.sleep(0.2)

    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False
        self._thread = threading.Thread(target=self.spawn_jars)
        self._thread.start()
        time.sleep(0.2)

    def close(self):
        pygame.mixer.music.stop()
        self.task = None
        self.jars = []
        self.timestamps = list(audio_processing.get_each_note(self.song))
        self.running = False
        open_window(self.game, "Game Over")()

    def lose_life(self):
        """Remove a heart anytime a jar is lost"""

        lives = self.elements.get("Lives")
        if len(lives) > 1:
            lives.pop()
        else:
            self.close()

    def update_elements(self, game):
        """Updates each element every frame."""
        if not self.paused:
            if self.pauseButton.is_pressed and self.running:
                self.pause()
            for name, element in self.elements.items():
                if name == "Lives":
                    continue
                element.on_update()
                if element.is_pressed:
                    if (
                        self._last_click is None
                        or perf_counter() - self._last_click > 0.2
                    ):
                        element.on_click()
                        self._last_click = perf_counter()

            for jar in self.jars:
                jar.move_down(self.speed)
                jar.on_update()
                if jar.is_pressed and not jar.broken:
                    self.smash(jar)
                    if "pickle" in str(jar.path):
                        self.lose_life()
                    else:
                        self.score += 100

                if jar.center[1] > HEIGHT and not jar.broken:
                    self.smash(jar)
                    if "pickle" not in str(jar.path):
                        self.lose_life()

                if jar.broken:
                    if jar.broken > 3 * FRAMES_PER_ANIMATION:
                        self.jars.remove(jar)
                        del jar
                    else:
                        fname = str(jar.path).split("/")[-1]
                        color = fname[: fname.index("J")]
                        jar.path = (
                            SPRITES
                            / f"{color}JarSmash{jar.broken // FRAMES_PER_ANIMATION}.png"
                        )
                        jar.broken += 1
        else:
            if self.pauseButton.is_pressed:
                self.unpause()

    def display_elements(self):
        """Display each element every frame."""
        SCREEN.blit(self._background, (0, 0))
        self.pauseButton.show()
        self.score_board.show()
        elements = [
            element for name, element in self.elements.items() if name != "Lives"
        ] + self.elements.get("Lives")
        for element in elements + self.jars:
            element.show()
        pygame.display.update()

    def smash(self, jar: gui.Button):
        """Destroys a specified jar"""

        smash_sound = pygame.mixer.Sound(self.smash_sound)
        volume = get_value("Effects Volume")
        smash_sound.set_volume(volume)
        smash_sound.play()
        self.score_board.message = self.score
        self.score_board.show()
        jar.broken = FRAMES_PER_ANIMATION

    async def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""
        while self.running and not self.paused:
            n = 3
            filename = random.choices(
                # Each color is n times more likely than a pickle
                ("pickle", "red", "purple", "magenta"),
                (1, n, n, n),
            )[0]
            self.jars.append(
                gui.Button(
                    SPRITES / f"{filename}Jar.png",
                    ((30 + (random.randint(0, 4) * 9)) * WIDTH // 103, 0),
                )
            )
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
