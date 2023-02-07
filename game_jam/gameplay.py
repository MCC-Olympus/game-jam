"""Classes and elements that will appear during the gameplay itself."""
import time
from time import perf_counter

import pygame

import gui
import audio_processing


class Level(gui.Window):
    """The class for making individual levels."""

    speed = 5
    WIDTH = pygame.display.Info().current_w
    HEIGHT = pygame.display.Info().current_h
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)

    def __init__(self, caption: str, song):
        super().__init__(caption)
        self.jars: list[gui.Button] = []
        self.timestamps, self.frequencies = audio_processing.get_each_note(song)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.start = time.perf_counter()

    def _update_elements(self):
        """Updates each element every frame."""
        for element in list(self.elements.values()) + self.jars:
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
                    jar.on_click(self)
                    self._last_click = perf_counter()
            if jar.center[1] > self.HEIGHT:
                self.jars.pop(0)
                del jar
                print("Game over")
                self.close()

    def _display_elements(self):
        """Display each element every frame."""
        Level.SCREEN.blit(self._background, (0, 0))
        for element in self.elements.values():
            element.show()
        for jar in self.jars:
            jar.show()
        pygame.display.update()
