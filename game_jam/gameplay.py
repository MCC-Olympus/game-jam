"""Classes and elements that will appear during the gameplay itself."""

import random
import sys
import threading
import time
from pathlib import Path
from time import perf_counter
import windows
import pygame

import audio_processing
import gui

ASSETS = Path(__file__).parent.parent / "assets"
SPRITES = ASSETS / "sprites"
SOUNDS = ASSETS / "sounds"
WIDTH = pygame.display.Info().current_w
class Level(gui.Window):
    """The class for making individual levels."""
    lives = []
    lives.append(gui.Button(SPRITES/"redHeart.png",(38,65),scale=3))
    lives.append(gui.Button(SPRITES/"redHeart.png",(147,65),scale=3))
    lives.append(gui.Button(SPRITES/"redHeart.png",(255,65),scale=3))
    WIDTH = pygame.display.Info().current_w
    HEIGHT = pygame.display.Info().current_h
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)
    score = 0

    def __init__(self, caption: str, song, speed=5):
        super().__init__(caption)
        self.jars: list[gui.Button] = []
        self.timestamps = list(audio_processing.get_each_note(song))
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
        self.start = time.perf_counter()
        self.speed = speed
        self.score = 0
        self.scoreBoard = gui.Text(message=str(self.score),position=(1000,200,200,100),border_radius=10,font_size=75)
        self.scoreBoard.show()
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
            self.close()
            pygame.quit()
            sys.exit()

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
                self.lose_life()
                self.smash(jar)

    def _display_elements(self):
        """Display each element every frame."""
        Level.SCREEN.blit(self._background, (0, 0))
        self.scoreBoard.show()
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
        del jar
        self.score +=100
        self.scoreBoard.message=self.score
        self.scoreBoard.show()
        


    def spawn_jars(self):
        """Generate the next jar in a random position in sync with the song."""
        while self._running:
            x = random.randint(0, 4)
            sprite = (
                Path(__file__).parent.parent / "assets" / "sprites" / "magentaJar.png"
            ) 
            self.jars.append(gui.Button(sprite, ((30+(x*9))*WIDTH // 103, 0)))
            sleep_amount = self.timestamps[1] - self.timestamps[0]
            time.sleep(sleep_amount)
            self.timestamps.pop()
