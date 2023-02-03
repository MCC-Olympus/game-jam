"""The entry point of the game."""

# Demo functionality
from gui import *
from audio_processing import get_each_note, play
from threading import Thread


def play_next_note(window):
    # play it in new thread
    button = window.get_element("play button")
    if button.times:
        Thread(
            target=play, args=(button.file, button.times.pop(0), button.times[0])
        ).start()


my_window = Window()
my_window.elements = {
    "play button": Button(
        SPRITE_PATH / "purpleJar.png",
        (WIDTH // 2, HEIGHT // 2),
        on_click=play_next_note,
    )
}

button = my_window.get_element("play button")
button.file = "../assets/sounds/ode-to-joy.wav"
button.times = list(get_each_note(button.file))


my_window.open()
