"""Classes and constants for creating the graphical user interface."""

from pathlib import Path

import pygame

import events

NAME = "JellySmash"

FPS = 60
ROOT_PATH = Path(__file__).parent.parent
SPRITE_PATH = ROOT_PATH / "assets/sprites"

pygame.init()

WIDTH = pygame.display.Info().current_w
HEIGHT = pygame.display.Info().current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)


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

        self.elements: dict[Element] = {}

    def _update_elements(self):
        """Updates each element every frame."""
        for element in self.elements.values():
            element.on_update(self)
            if isinstance(element, Button) and element._is_pressed:
                element.on_click(self)
                pygame.time.wait(200)

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
                    events.exit_game(self)

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


class Element:
    """Base class for all UI elements"""

    def __init__(
        self,
        position: tuple[int, int, int, int],
        border_radius=50,
        on_update=lambda element: None,
    ):
        self.on_update = on_update
        self.position = position
        self._rect = pygame.Rect(position)
        self.center = self._rect.center
        self._border_radius = border_radius

    @property
    def _is_pressed(self):
        """Determine whether the mouse is pressing an element."""
        return pygame.mouse.get_pressed()[0] and self._rect.collidepoint(
            pygame.mouse.get_pos()
        )

    def show(self):
        """Display an element to the screen"""
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self._rect, border_radius=self._border_radius
        )


class Button(Element):
    """A type of UI element that has text as well as click event handling."""

    def __init__(
        self,
        prompt: str,
        position: tuple[int, int, int, int],
        border_radius=50,
        font_size=30,
        on_update=lambda element: None,
        on_click=lambda element: None
    ):
        super().__init__(position, border_radius, on_update=on_update)
        self._message = prompt
        self._border_radius = border_radius
        self._font_size = font_size
        self.on_click = on_click

    def show(self):
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self._rect, border_radius=self._border_radius
        )
        font = pygame.font.get_default_font()
        text = pygame.font.Font(font, self._font_size).render(
            self._message, True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = self.center
        SCREEN.blit(text, text_rect)
