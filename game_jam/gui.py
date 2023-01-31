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

    def __init__(self, caption: str = NAME):
        self.background = pygame.transform.scale(
            pygame.image.load(SPRITE_PATH / "JellyJam.png").convert(),
            (WIDTH, HEIGHT),
        )

        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.elements: dict[Element] = {}
        self._running = False

    def update_elements(self):
        """Updates each element every frame."""
        for element in self.elements.values():
            element.on_update(self)
            if isinstance(element, Button) and element.is_pressed:
                element.on_click(self)
                pygame.time.wait(200)

    def display_elements(self):
        """Display each element every frame."""
        SCREEN.blit(self.background, (0, 0))
        for element in self.elements.values():
            element.show()
        pygame.display.update()

    def on_update(self):
        """Special functionality that must be ran once each frame."""

    def loop(self):
        """Determines what the window does each frame and when the window closes."""
        while self._running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    events.exit_game(self)

            self.on_update()
            self.update_elements()
            self.display_elements()

    def open(self):
        """Starts the window."""
        self._running = True
        self.loop()

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
        self.rect = pygame.Rect(position)
        self.center = self.rect.center
        self.border_radius = border_radius

    @property
    def is_pressed(self):
        """Determine whether or not the mouse is pressing an element."""
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()
        )


    def show(self):
        """Display an element to the screen"""
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self.rect, border_radius=self.border_radius
        )


class Button(Element):
    """A type of UI element that has text as well as click event handling."""
    def __init__(
        self,
        prompt: str,
        position: tuple[int, int, int, int],
        border_radius=50,
        on_click=lambda element: None,
    ):
        super().__init__(position, border_radius)
        self.message = prompt
        self.border_radius = border_radius
        self.font_size = 30
        self.on_click = on_click

    def show(self):
        pygame.draw.rect(
            SCREEN, (140, 140, 140), self.rect, border_radius=self.border_radius
        )
        font = pygame.font.get_default_font()
        text = pygame.font.Font(font, self.font_size).render(
            self.message, True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = self.center
        SCREEN.blit(text, text_rect)
