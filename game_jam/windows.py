"""Graphical elements that make up the graphical user interface. Should only contain data"""

from events import *
from gui import *
from values import Defaults
from constants import *

song_volume = Defaults.song_volume
effect_volume = Defaults.effect_volume


def lvl_one_load(window: Window):
    window.close()
    level_one.open()


def lvl_two_load(window: Window):
    window.close()
    level_two.open()


def lvl_three_load(window: Window):
    window.close()
    level_three.open()


menu = Window(caption="JellySmash Menu", background=SPRITES/"sbg.png")
menu.elements = {
    "open": Button(SPRITES / "startButton.png",(WIDTH // 2 - 100, 100),scale=2, on_click=open_level_select),
    "settings": Button(SPRITES / "settingsButton.png",(WIDTH // 2 - 150, 300),scale=2, on_click=open_settings),
    "exit": Button(SPRITES / "exitButton.png",(WIDTH // 2 - 50, 500),scale=2, on_click=exit_game),
}
level_select = Window(caption="Level selector", background=SPRITES / "bg.png")
level_select.elements = {
    "Level One": Button(SPRITES / "lvlOneButton.png", (WIDTH // 5 - 100, HEIGHT//4),border_radius=0, angle=0, scale=3, on_click=lvl_one_load),
    "Level Two": Button(SPRITES / "lvlTwoButton.png", (2*WIDTH // 5 - 100, HEIGHT//4),border_radius=0, angle=0, scale=3,on_click=lvl_two_load),
    "Level Three": Button(SPRITES / "lvlThreeButton.png", (3*WIDTH // 5 - 100, HEIGHT//4), border_radius=0, angle=0, scale=3,on_click=lvl_three_load),
    "Endless Mode": Button(SPRITES / "endlessButton.png", (4*WIDTH // 5 - 100, HEIGHT//4), angle=0, scale=3,on_click=to_menu),
    "Back": Button(SPRITES / "backButton.png", (WIDTH // 2 - 100, 2*HEIGHT//4), angle=0, scale=3, on_click=to_menu)
}

settings = Window(caption="JellySmash Settings", background=SPRITES/"bg.png")
settings.elements = {
    "increase_song": TextButton(">", (WIDTH // 2 + 125, 200, 50, 50,), on_click=increase_song_volume),
    "decrease_song": TextButton("<", (WIDTH // 2 - 175, 200, 50, 50), on_click=decrease_song_volume),
    "increase_effect": TextButton(">", (WIDTH // 2 + 125, 300, 50, 50,), on_click=increase_effect_volume),
    "decrease_effect": TextButton("<", (WIDTH // 2 - 175, 300, 50, 50), on_click=decrease_effect_volume),
    "Music": TextButton(f"Music: {Defaults.song_volume * 100:.0f}", (WIDTH // 2 - 100, 200, 200, 50), on_update=update_song_volume,
                        on_click=reset_song_volume),
    "effects": TextButton(f"Effects: {Defaults.effect_volume * 100:.0f}", (WIDTH // 2 - 100, 300, 200, 50), on_update=update_effect_volume,
                        on_click=reset_effect_volume),
    "back": TextButton("Back", (WIDTH // 2 - 100, 400, 200, 50), on_click=to_menu),
}

level_one = Window("Level One screen",score=0)
level_one.elements = {
    "Belt One": Button(SPRITES / "belt.png",(29*WIDTH // 103 , 0),0,scale=(HEIGHT/get_sprite_height("belt.png"))),
    "Belt Two": Button(SPRITES / "belt.png",(38*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png"))),
    "Belt Three": Button(SPRITES / "belt.png",(47*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png"))),
    "Belt Four": Button(SPRITES / "belt.png",(56*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png"))),
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
