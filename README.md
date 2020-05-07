# PythonGameOfLife
A simple cellular automaton using the pygame and numpy libraries on the Anaconda 3 Environment

This is my first complete python project that I made for fun and to try out the pygame library and some class and object use 😊

The automaton uses the rules of Conway's Game of Life in the "Classic Mode" which are shown here: https://en.wikipedia.org/wiki/Cellular_automaton
The "Variant Mode" introduces the rule that dead cells with 3 neighbors are also born which leads to very rapid growth from simple starting
conditions.

While paused you can click on a cell to change its state in order to draw the initial conditions u want.
As well as the on-screen buttons one may use the following hotkeys:

ENTER - pause/unpause  
SPACE - run 1 step  
R - do random initial configuration  
X - clear board  


The game set up and main loop is run in main.py using functions defined in confunct.py and creating an object-oriented user interface
with the classed defined in conUI.py  
An executable is provided for windows users who don't have python and pygame installed. To generate the executable I used Pyinstaller
but i've still got a lot to learn on packaging python applications. The executable is quite heavy (around 200 MB) and takes quite a while
to load. Any resources on how to properly package executables and installer would be very welcome 👍
