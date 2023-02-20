# Jelly Smash

An MCC INFO1325-WI Game Jam entry from the Olympus team.

## Deacription

You must try to collect as much precious jam as you can before it shatters on the floor! Click on jars of jelly to increase your score. Avoid the pickle jars, so you don't ruin your jam collection. Good luck!

The jars fall in time with three different songs, including Ode to Joy and RushE.

## How To Play

There's two wys you can play the game: in your browser or by running the source. 

Running it in the browser is the simplest way, but performance tends to be worse and more inconsistant.

### Web Interface

You can play the game directly in your browser by [clicking this link](https://mcc-olympus.github.io/game-jam/).

This redirects you to this repository's github pages site. The game is deployed using [pygbag](https://github.com/pygame-web/pygbag), a Python interpreter for running code in WebAssembly in the browser.

### Source Code

First you need to [install Python](https://www.python.org/downloads/release/python-3109/)

Then, open up a twrminal window and install the [PyGame](https://www.pygame.org/) module with this command:
```
py -m pip install pygame
```
> Note: If you installed Python 3.11, PyGame is not yet fully released, so you need to add the `--pre` flag to the install command.

Next, you need to clone this repository onto your computer. Run the following commands in the folder you want to install the game in:
```
git clone https://github.com/MCC-Olympus/game-jam.git
cd game-jam
```

Finally, run the main file.
```
py -m main
```
