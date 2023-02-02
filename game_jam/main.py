"""The entry point of the game."""
from events import *
from gui import *


# This is demo code that shows how to use the classes and functions to create a GUI window

def say_hi(window: Window):
    """Shows this every time the jar is clicked."""
    print("hi :D")


def rotate(window: Window):
    """Does this every frame"""
    window.get_element("spinning jar").angle += 1


# Create instance of the window class
my_window = Window(caption="Demo")
my_window.elements = {
    "title": Text("Demo of UI", (WIDTH // 2, HEIGHT // 3, 0, 0), font_size=50, color=(255, 0, 0)),
    # Add a button called "test" to the window
    "spinning jar": Button(SPRITE_PATH / "purpleJar.png", (WIDTH // 2, HEIGHT // 2,), on_click=to_menu, on_update=rotate)
}

my_window.open()
