"""Classes and elements that will appear during the gameplay itself."""

import random
import threading
import time
from pathlib import Path
from time import perf_counter

import pygame

import audio_processing
import gui


class Level(gui.Window):
    """The class for making individual levels."""

    speed = 5
    WIDTH = pygame.display.Info().current_w
    HEIGHT = pygame.display.Info().current_h
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)

    def __init__(self, caption: str, song):
        super().__init__(caption)
        self.jars: list[gui.Button] = []
        self.timestamps = list(audio_processing.get_each_note(song))
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.start = time.perf_counter()

        self._running = True
        self._thread = threading.Thread(target=self.spawn_jars)
        self._thread.start()

    def _update_elements(self):
        """Updates each element every frame."""
        for element in self.elements.values():
            element.on_update(self)
            if element.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    element.on_click(self)
                    self._last_click = perf_counter()

        for jar in self.jars:
            jar.move_down(Level.speed)
            # Check it's in bounds
            jar.on_update(self)
            if jar.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    self.smash(jar)
                    self._last_click = perf_counter()
            if jar.center[1] > self.HEIGHT:
                print("Game over")
                self._running = False
                self.close()

    def _display_elements(self):
        """Display each element every frame."""
        Level.SCREEN.blit(self._background, (0, 0))
        for element in self.elements.values():
            element.show()
        for jar in self.jars:
            jar.show()
        pygame.display.update()

    def smash(self, jar: gui.Button):
        """Destroys a specified jar"""
        self.jars.pop(self.jars.index(jar))
        del jar

    def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""
        while self._running:
            x = random.randint(0, self.HEIGHT - 100)
            sprite = (
                Path(__file__).parent.parent / "assets" / "sprites" / "magentaJar.png"
            )
            self.jars.append(gui.Button(sprite, (x, 0)))

            sleep_amount = self.timestamps[1] - self.timestamps[0]
            time.sleep(sleep_amount)
            self.timestamps.pop()
