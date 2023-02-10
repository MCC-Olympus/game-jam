"""Classes and elements that will appear during the gameplay itself."""

import random
import threading
import time
from time import perf_counter

import audio_processing
import gui
import windows
from constants import *


class Level(gui.Window):
    """The class for making individual levels."""

    def __init__(self, caption: str, song, speed=5):
        super().__init__(caption)
        self.jars: list[gui.Button] = []
        self.timestamps = list(audio_processing.get_each_note(song))
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.smash_sound = SOUNDS / "smashing_glass.wav"

        self.start = time.perf_counter()
        self.speed = speed
        self.score = 0

        self.lives = [
            gui.Button(SPRITES / "redHeart.png", (38, 65), scale=3),
            gui.Button(SPRITES / "redHeart.png", (147, 65), scale=3),
            gui.Button(SPRITES / "redHeart.png", (255, 65), scale=3),
        ]
        self.score = 0

        self.score_board = gui.Text(
            message=str(self.score),
            position=(997, 201, 355, 100),
            border_radius=0,
            font_size=75,
        )
        self.score_board.show()
        self._running = True
        self._thread = threading.Thread(target=self.spawn_jars)
        self._thread.start()

    def close(self):
        super().close()
        windows.level_select.open()

    def lose_life(self):
        """Remove a heart anytime a jar is lost"""

        if len(self.lives) > 1:
            self.lives.pop()
        else:
            print("Game over")
            self._running = False
            pygame.mixer.music.stop()
            self.close()

    def _update_elements(self):
        """Updates each element every frame."""
        for element in self.elements.values():
            element.on_update(self)
            if element.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    element.on_click(self)
                    self._last_click = perf_counter()

        for jar in self.jars:
            jar.move_down(self.speed)
            # Check it's in bounds
            jar.on_update(self)
            if jar.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    self.smash(jar)
                    if "pickle" in str(jar.path):
                        self.lose_life()
                    else:
                        self.score += 100
                    self._last_click = perf_counter()
            if jar.center[1] > HEIGHT:
                self.smash(jar)
                if "pickle" not in str(jar.path):
                    self.lose_life()

    def _display_elements(self):
        """Display each element every frame."""
        SCREEN.blit(self._background, (0, 0))
        self.score_board.show()
        for element in (
            list(self.elements.values())
            + list(windows.level_one.elements.values())
            + self.jars
            + self.lives
        ):
            element.show()
        pygame.display.update()

    def smash(self, jar: gui.Button):
        """Destroys a specified jar"""

        pygame.mixer.Sound(self.smash_sound).play()
        self.jars.pop(self.jars.index(jar))
        del jar
        self.score_board.message = self.score
        self.score_board.show()

    def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""
        while self._running:
            filename = random.choices(
                # Each color is 3x more likely than a pickle
                ("pickle", "red", "purple", "magenta"), (1, 3, 3, 3)
            )[0]
            self.jars.append(
                gui.Button(
                    SPRITES / f"{filename}Jar.png",
                    ((30 + (random.randint(0, 4) * 9)) * WIDTH // 103, 0),
                )
            )
            notes = len(self.timestamps)
            if notes >= 2:
                time.sleep(self.timestamps[1] - self.timestamps[0])
            elif notes == 1:
                time.sleep(self.timestamps[0])
            else:
                print("You win!")
                self.close()
            self.timestamps.pop()
