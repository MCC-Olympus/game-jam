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

    def lose_life(self):
        """Remove a heart anytime a jar is lost"""
        if len(self.lives) > 1:
            self.lives.pop()
        else:
            print("Game over")
            self._running = False
            pygame.mixer.music.stop()
            self.close()
            from windows import level_select
            level_select.open()

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
                    self._last_click = perf_counter()
            if jar.center[1] > self.HEIGHT:
                self.jars.pop(self.jars.index(jar))
                color = str(jar.path)
                del jar
                if "pickelJar.png" in color:
                    pass
                else:
                    self.lose_life()
                self.lose_life()
                self.smash(jar)

    def _display_elements(self):
        """Display each element every frame."""
        SCREEN.blit(self._background, (0, 0))
        self.score_board.show()
        for element in self.elements.values():
            element.show()
        for element in windows.level_one.elements.values():
            element.show()
        for jar in self.jars:
            jar.show()
        for life in self.lives:
            life.show()
        pygame.display.update()

    def smash(self, jar: gui.Button):
        """Destroys a specified jar"""
        self.jars.pop(self.jars.index(jar))
        color = str(jar.path)
        del jar
        if "pickelJar.png" in color:
            self.lose_life()
        else:
            self.score +=100
        self.scoreBoard.message=self.score
        self.scoreBoard.show()
        


    def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""
        while self._running:
            x = random.randint(0, 4)
            z = random.randint(1,100)
            if z < 11: daColor = "pickelJar.png"
            elif z < 41: daColor = "redJar.png"
            elif z < 71: daColor = "magentaJar.png"
            else: daColor = "purpleJar.png"
            sprite = (
                SPRITES / daColor
            )
            self.jars.append(gui.Button(sprite, ((30 + (x * 9)) * WIDTH // 103, 0)))
            sleep_amount = self.timestamps[1] - self.timestamps[0]
            time.sleep(sleep_amount)
            self.timestamps.pop()
