"""Events that are triggered for a specific object every frame."""

import json

import pygame

from .constants import GAME_JAM, Function, FRAMES_PER_ANIMATION, HEIGHT, SPRITES
from .gui import Window, Element

SETTINGS = GAME_JAM / "settings.json"


def get_window(game, window_name) -> Window:
    """
    Gives a Window object from the parent Game object.

    :param game: The Game object that contains the window.
    :param window_name: The name of the desired window.
    """

    return game.get_window(window_name)


def get_element(game, window_name, element_name) -> Element:
    """
    Returns an Element object from its parent objects.

    :param game: The game object the element is in.
    :param window_name: The name of the window in the game object that holds the element.
    :param element_name: The name of the element.
    """

    return game.get_window(window_name).get_element(element_name)


def open_window(game, name: str) -> Function:
    """
    Open a specified game window.

    :param game: The game object that holds the window.
    :param name: The name of the window, specified as a key in the dictionary `game.windows`.
    """

    def inner():
        pygame.time.wait(200)
        game.open(name)

    return inner


def get_settings() -> dict[str:float]:
    """
    Gives a dictionary of the settings file.
    """

    with SETTINGS.open() as file:
        data = json.load(file)
    return data


def get_value(key: str) -> float:
    """
    Get the specified key from the settings file.

    :param key: The setting to retrieve the value from.
    """

    return get_settings().get(key)


def set_setting(key: str, value: float) -> None:
    """
    Set the given setting to be a new value.

    :param key: The setting to be changed.
    :param value: The new value of the setting.
    """

    if value < 0:
        value = 0
    elif value > 1:
        value = 1

    data = get_settings()
    data[key] = value
    with SETTINGS.open("w") as file:
        json.dump(data, file)


def exit_game(game) -> Function:
    """Closes the game and thanks the player."""

    def inner():
        game.exit()

    return inner


def increase_volume(volume_type: str) -> Function:
    """Increase the volume by 0.1, if possible."""

    def inner():
        key = f"{volume_type} Volume"
        old_volume = get_settings().get(key)
        new_volume = min(old_volume + 0.1, 1)
        set_setting(key, new_volume)

    return inner


def decrease_volume(volume_type: str) -> Function:
    """Decrease the volume by 0.1, if possible."""

    def inner():
        key = f"{volume_type} Volume"
        old_volume = get_settings().get(key)
        new_volume = min(old_volume - 0.1, 1)
        set_setting(key, new_volume)

    return inner


def reset_volume(volume_type: str) -> Function:
    """Either mutes the volume or sets it to halfway, depending on how it currently is."""

    def inner():
        key = f"{volume_type} Volume"
        old_volume = get_settings().get(key)
        new_volume = 0
        if old_volume == 0:
            new_volume = 0.5
        set_setting(key, new_volume)

    return inner


def update_volume(game, window_name: str, volume_type: str) -> Function:
    """Makes the buttons in settings display the volume in real time."""

    def inner():
        key = f"{volume_type} Volume"
        elem = get_element(game, window_name, key)
        elem.message = f"Music: {get_value(key) * 100:.0f}"

    return inner


def toggle_paused(level) -> Function:
    """Pause or resume the game."""

    def inner():
        print("pressed")
        if level.running:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        level.running = not level.running

    return inner


def update_scoreboard(level):
    def inner():
        level.get_element("Score board").message = level.score

    return inner


def update_jar(level, jar, y: int):
    """Move the element down by the specified amount."""

    def inner(jar=jar):
        jar.move(0, y)
        if jar.center[1] > HEIGHT and not jar.broken:
            smash(level, jar)
            if "pickle" not in str(jar.path):
                level.lose_life()

        if jar.broken:
            if jar.broken > 3 * FRAMES_PER_ANIMATION:
                jars = level.elements.get("Jars")
                jars.remove(jar)
                del jar
            else:
                filename = str(jar.path).rsplit("/", maxsplit=1)[-1]
                color = filename[: filename.index("J")]
                jar.path = (
                    SPRITES / f"{color}JarSmash{jar.broken // FRAMES_PER_ANIMATION}.png"
                )
                jar.broken += 1

    return inner


def smash_jar(level, jar):
    """Destroy a given jar."""

    def inner():
        if not jar.broken:
            smash(level, jar)
            if "pickle" in str(jar.path):
                level.lose_life()
            else:
                level.score += 100

    return inner


def smash(level, jar):
    """Destroy a jar."""

    smash_sound = pygame.mixer.Sound(level.smash_sound)
    volume = get_value("Effects Volume")
    smash_sound.set_volume(volume)
    smash_sound.play()

    jar.broken = FRAMES_PER_ANIMATION
