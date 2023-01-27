import sys
from pathlib import Path

import pygame

FPS = 60
ROOT_PATH = Path(__file__).parent.parent
SPRITE_PATH = ROOT_PATH / "assets/sprites"

pygame.init()

WIDTH, HEIGHT = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h,
)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE)


class Window:
    def __init__(self):
        self.BACKGROUND = pygame.transform.scale(
            pygame.image.load(SPRITE_PATH / "JellyJam.png").convert(),
            (WIDTH, HEIGHT),
        )

        pygame.display.set_caption("Jelly Jam")

        self.clock = pygame.time.Clock()

        self.elements = {}

    def display_elements(self):
        SCREEN.blit(self.BACKGROUND, (0, 0))

        for element in self.elements.values():
            element.show()

        pygame.display.update()


def exit_game() -> None:
    print("Thanks for playing!")
    pygame.quit()
    sys.exit()


class Menu(Window):
    def __init__(self, volume=0.5):
        super().__init__()

        pygame.display.set_caption("Jelly Jam Menu")

        self.volume = volume

        self.elements = {
            "start": Button("Start", (WIDTH // 2 - 100, 200, 200, 50)),
            "settings": Button("Settings", (WIDTH // 2 - 100, 300, 200, 50)),
            "exit": Button("Exit", (WIDTH // 2 - 100, 400, 200, 50)),
        }

    def handle_button_presses(self) -> None:
        for name, element in self.elements.items():
            if element.is_pressed:
                if name == "start":
                    # Start the game
                    ...
                elif name == "settings":
                    Settings().start_loop()
                elif name == "exit":
                    exit_game()

    def start_loop(self):
        while True:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()

            self.handle_button_presses()
            self.display_elements()


class Button:
    def __init__(
        self,
        prompt: str,
        position: tuple[int, int, int, int],
        border_radius=50,
    ):
        self.position = position
        self.message = prompt
        self.rect = pygame.Rect(position)
        self.center = self.rect.center
        self.border_radius = border_radius
        self.font_size = 30

    @property
    def is_pressed(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(
            pygame.mouse.get_pos()
        )

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


class Settings(Menu):
    def __init__(self):
        super().__init__()

        self.elements = {
            "increase_sound": Button(
                "->",
                (
                    WIDTH // 2 + 125,
                    200,
                    50,
                    50,
                ),
            ),
            "decrease_sound": Button("<-", (WIDTH // 2 - 175, 200, 50, 50)),
            "sound": Button(
                f"Sound: {self.volume * 100:.0f}",
                (WIDTH // 2 - 100, 200, 200, 50),
            ),
            "back": Button("Back", (WIDTH // 2 - 100, 400, 200, 50)),
        }

    def handle_button_presses(self) -> None:
        for name, element in self.elements.items():
            if element.is_pressed:
                if name == "increase_sound":
                    self.volume += 0.1
                elif name == "decrease_sound":
                    self.volume -= 0.1
                elif name == "sound":
                    if self.volume == 0:
                        self.volume = 0.5
                    else:
                        self.volume = 0
                elif name == "back":
                    pygame.time.wait(200)
                    Menu().start_loop()

                pygame.time.wait(200)

    def start_loop(self):
        while True:
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()

            self.handle_button_presses()

            if self.volume > 1:
                self.volume = 1
            elif self.volume < 0:
                self.volume = 0

            self.elements["sound"].message = f"Sound: {self.volume * 100:.0f}"

            self.display_elements()
