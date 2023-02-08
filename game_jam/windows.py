"""Graphical elements that make up the graphical user interface. Should only contain data"""

from events import *
from gui import *
from values import Defaults

volume = Defaults.volume

menu = Window(caption="JellySmash Menu", background=SPRITE_PATH/"JellyJam.png")
menu.elements = {
    "open": TextButton("Start", (WIDTH // 2 - 100, 200, 200, 50), on_click=open_level_select),
    "settings": TextButton("Settings", (WIDTH // 2 - 100, 300, 200, 50), on_click=open_settings),
    "exit": TextButton("Exit", (WIDTH // 2 - 100, 400, 200, 50), on_click=exit_game),
}
level_select = Window(caption="Level selector")
level_select.elements = {
    "Level One": Button(SPRITE_PATH / "lvlOneButton.png",(WIDTH // 5 -100, 300),0,on_click=lvl_load),
    "Level Two": Button(SPRITE_PATH / "lvlTwoButton.png",(2*WIDTH // 5 -100, 300),0,on_click=to_menu), 
    "Level Three": Button(SPRITE_PATH / "lvlThreeButton.png",(3*WIDTH // 5 -100, 300),0,on_click=to_menu),
    "Endless Mode": Button(SPRITE_PATH / "endlessButton.png",(4*WIDTH // 5 -100, 300),0,on_click=to_menu)
}

settings = Window(caption="JellySmash Settings", background=SPRITE_PATH/"JellyJam.png")
settings.elements = {
    "increase_sound": TextButton("->", (WIDTH // 2 + 125, 200, 50, 50,), on_click=increase_volume),
    "decrease_sound": TextButton("<-", (WIDTH // 2 - 175, 200, 50, 50), on_click=decrease_volume),
    "sound": TextButton(f"Sound: {Defaults.volume * 100:.0f}", (WIDTH // 2 - 100, 200, 200, 50), on_update=update_volume,
                        on_click=reset_sound),
    "back": TextButton("Back", (WIDTH // 2 - 100, 400, 200, 50), on_click=to_menu),
}

level_one = Window("Level One")
level_one.elements = {
    "Belt One": Button(SPRITE_PATH / "belt.png",(29*WIDTH // 103 , 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Two": Button(SPRITE_PATH / "belt.png",(38*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Three": Button(SPRITE_PATH / "belt.png",(47*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Four": Button(SPRITE_PATH / "belt.png",(56*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_click=do_nothing),
    "Belt Five": Button(SPRITE_PATH / "belt.png",(65*WIDTH // 103, 0),0,scale=(HEIGHT/get_sprite_height("belt.png")),on_update=lvl_one_run),
}
