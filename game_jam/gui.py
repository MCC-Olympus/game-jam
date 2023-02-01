"""Classes and constants for creating the graphical user interface."""

import sys
import time
from pathlib import Path
from time import perf_counter
from types import FunctionType

import pygame

NAME = "JellySmash"

FPS = 60
ROOT_PATH = Path(__file__).parent.parent
SPRITE_PATH = ROOT_PATH / "assets/sprites"

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)

# Type hints
Cordinate = tuple[int, int]
RGB = tuple[int, int, int]
Rect = tuple[int, int, int, int]


class Window:
    """Base class for creating all GUI windows."""

    def __init__(self, caption: str = NAME, on_update=lambda: None):
        pygame.display.set_caption(caption)

        self._background = pygame.transform.scale(
            pygame.image.load(SPRITE_PATH / "JellyJam.png").convert(),
            (WIDTH, HEIGHT),
        )
        self._clock = pygame.time.Clock()
        self._running = False
        self._on_update = on_update
        self._last_click = None

        self.elements: dict[Element] = {}

    def _update_elements(self):
        """Updates each element every frame."""
        for element in self.elements.values():
            element.on_update(self)
            if element.is_pressed:
                if self._last_click is None or perf_counter() - self._last_click > 0.2:
                    element.on_click(self)
                    self._last_click = time.perf_counter()

    def _display_elements(self):
        """Display each element every frame."""
        SCREEN.blit(self._background, (0, 0))
        for element in self.elements.values():
            element.show()
        pygame.display.update()

    def _loop(self):
        """Determines what the window does each frame and when the window closes."""
        while self._running:
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Thanks for playing!")
                    pygame.quit()
                    sys.exit()

            self._on_update()
            self._update_elements()
            self._display_elements()

    def open(self):
        """Starts the window."""
        self._running = True
        self._loop()

    def close(self):
        """Stop the window.."""
        self._running = False

    def get_element(self, name: str) -> 'Element':
        return self.elements[name]


class Element:
    """The base UI object from which all others are made from."""

    def __init__(
        self,
        position: Rect,
        border_radius=50,
        on_update: FunctionType = None
    ):
        if on_update is not None:
            self.on_update = on_update
        self.position = position
        self._rect = pygame.Rect(position)
        self.center = self._rect.center
        self._border_radius = border_radius

    def show(self):
        """Display an element to the screen"""
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self._rect, border_radius=self._border_radius
        )

    @property
    def is_pressed(self):
        """Determine whether the mouse is pressing an element."""
        return pygame.mouse.get_pressed()[0] and self._rect.collidepoint(
            pygame.mouse.get_pos()
        )

    def on_click(self):
        """Called when an element is clicked on"""

    @staticmethod
    def on_update(window: Window):
        """Called every frame."""


class Text(Element):
    """Display text to the window."""

    def __init__(
        self, message: str,
        position: Rect,
        color: RGB = (0, 0, 0),
        border_radius=50, font_size=30,
        on_update: FunctionType = None
    ):
        super().__init__(position, border_radius, on_update)
        self.message = message
        self.color = color
        self._border_radius = border_radius
        self._font_size = font_size

    def show(self):
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self._rect, border_radius=self._border_radius
        )
        font = pygame.font.get_default_font()
        text = pygame.font.Font(font, self._font_size).render(
            self.message, True, self.color
        )
        text_rect = text.get_rect()
        text_rect.center = self.center
        SCREEN.blit(text, text_rect)


class TextButton(Text):
    """A button that shows text rather than an image."""

    def __init__(
        self,
        message: str,
        position: Rect,
        color: RGB = (0, 0, 0),
        border_radius=50,
        font_size=30,
        on_update: FunctionType = None,
        on_click: FunctionType = None
    ):
        super().__init__(message, position, color, border_radius, font_size, on_update)
        if on_click is not None:
            self.on_click = on_click

    @staticmethod
    def on_click(window: Window):
        """Called whenever the button is pressed"""


class Button(Element):
    """A UI element that displays an image and performs an action when clicked."""

    def __init__(
        self,
        path: Path,
        top_left: Cordinate,
        border_radius=50,
        angle=0,
        on_update: FunctionType = None,
        on_click: FunctionType = None
    ):
        self._sprite = pygame.image.load(path)
        self.angle = angle
        super().__init__(self._sprite.get_rect().move(top_left), border_radius, on_update)
        if on_click is not None:
            self.on_click = on_click

    def show(self):
        image = pygame.transform.rotate(self._sprite, self.angle)
        rect = image.get_rect(center=self.center)

        SCREEN.blit(image, rect)

    def on_click(self):
        """Called whenever the button is pressed"""
