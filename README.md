# Haunted Office
A game where you're just trying to have a normal day and ghosts ruin everything.

## Features
The user has to get a certain number of points within a time limit. Points are earned by moving a character around the screen to touch the pink squares using the arrow keys or WASD. There are also ghosts that follow the player around. The player can't move for 2 seconds if they are touched by a ghost.

## Installation
- Pygame Zero and Pygame are used to design video games in Python

Use the pip to install Pygame Zero ([this will also install Pygame](https://pygame-zero.readthedocs.io/en/stable/installation.html)).
```bash
pip install pgzrun
```

## Known Bugs
- Ghosts sometimes begin to overlap or stick to player if the player doesn't move for several seconds
- Ghost image sometimes doesn't update when ghost changes direction
- Player can sometimes move through ghosts without being frozen

## Cheat codes
- To jump to the end of a level, click anywhere while pressing Z
- To teleport to the mouse, click anywhere while pressing X (Warning: you won't be able to move if you teleport into an obstacle)

## Sources

#### Sources used for learning concepts:

https://pygame-zero.readthedocs.io/en/stable/builtins.html - Used to learn about classes in the Pygame Zero module.

https://www.pygame.org/docs/ref/rect.html - Used to learn how to use methods for the Pygame Rect class.

https://pygame-zero.readthedocs.io/en/stable/hooks.html - Documentation of pgzero event hooks. Used to learn how to schedule events such as the end of a level, the end of the ghost freeze effect, and others.

https://docs.python.org/3/library/random.html - Used to learn how to use the randint function.

https://www.w3schools.com/python/python_ref_list.asp - Used to verify how to use various Python list methods.

https://pygame-zero.readthedocs.io/en/stable/ptext.html - Used to learn how to display text in Pygame Zero.

#### Code used in game:

https://stackoverflow.com/questions/134934/display-number-with-leading-zeros - Used to format the time remaining in a level with a leading zero.

https://pythonprogramming.net/making-interactive-pygame-buttons/?completed=/pygame-buttons-part-1-button-rectangle/ - Used to get the position of the mouse to make buttons.

#### Fonts:

https://fonts.google.com/specimen/Barlow#standard-styles - Font used for almost all text in game

https://www.dafont.com/doctor-glitch.font - Font used for game title and at the end of the game
