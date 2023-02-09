"""Graphical elements that make up the graphical user interface. Should only contain data"""

from events import *
from gui import *
from values import Defaults
from constants import *

volume = Defaults.volume


def lvl_one_load(window: Window):
    window.close()
    level_one.open()


def lvl_two_load(window: Window):
    window.close()
    level_two.open()


def lvl_three_load(window: Window):
    window.close()
    level_three.open()

menu = Window(caption="JellySmash Menu", background=SPRITE_PATH/"sbg.png")
menu.elements = {
    "open": Button(SPRITES / "startButton.png",(WIDTH // 2 - 100, 100),scale=2, on_click=open_level_select),
    "settings": Button(SPRITES / "settingsButton.png",(WIDTH // 2 - 100, 300),scale=2, on_click=open_settings),
    "exit": Button(SPRITES / "exitButton.png",(WIDTH // 2 - 100, 500),scale=2, on_click=exit_game),
}
level_select = Window(caption="Level selector", background=SPRITES / "bg.png")
level_select.elements = {
    "Level One": Button(SPRITES / "lvlOneButton.png", (WIDTH // 5 - 100, 300),border_radius=0, angle=0, scale=3, on_click=lvl_one_load),
    "Level Two": Button(SPRITES / "lvlTwoButton.png", (2*WIDTH // 5 - 100, 300),border_radius=0, angle=0, scale=3,on_click=lvl_two_load),
    "Level Three": Button(SPRITES / "lvlThreeButton.png", (3*WIDTH // 5 - 100, 300), border_radius=0, angle=0, scale=3,on_click=lvl_three_load),
    "Endless Mode": Button(SPRITES / "endlessButton.png", (4*WIDTH // 5 - 100, 300), angle=0, scale=3,on_click=to_menu),
    "Back": Button(SPRITES / "exitButton.png", (WIDTH // 2 - 100, 500), angle=0, scale=3, on_click=to_menu)
}

settings = Window(caption="JellySmash Settings", background=SPRITES/"JellyJam.png")
settings.elements = {
    "increase_sound": TextButton("->", (WIDTH // 2 + 125, 200, 50, 50,), on_click=increase_volume),
    "decrease_sound": TextButton("<-", (WIDTH // 2 - 175, 200, 50, 50), on_click=decrease_volume),
    "sound": TextButton(f"Sound: {Defaults.volume * 100:.0f}", (WIDTH // 2 - 100, 200, 200, 50), on_update=update_volume,
                        on_click=reset_sound),
    "back": TextButton("Back", (WIDTH // 2 - 100, 400, 200, 50), on_click=to_menu),
}

level_one = Window("Level One screen",score=0)
level_one.elements = {
    "Belt One": Button(SPRITES / "belt.png",(29*WIDTH // 103 , 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Two": Button(SPRITES / "belt.png",(38*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Three": Button(SPRITES / "belt.png",(47*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Four": Button(SPRITES / "belt.png",(56*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Five": Button(SPRITES / "belt.png",(65*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_update=lvl_one_run),
}

level_two = Window("Level Two screen")
level_two.elements = {
    "Belt Five": Button(SPRITES / "belt.png", (65*WIDTH // 103, 0), 0, scale=(HEIGHT/get_sprite_height("belt.png")), on_update=lvl_two_run),
}

level_three = Window("Level Three screen")
level_three.elements = {
    "Belt Five": Button(SPRITES / "belt.png",(65*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_update=lvl_three_run),
}
