# Switch Box Routing Simulation Environment ##

## Overview ##
### graphics.py ###
A simple, open-source graphics library, build on top of Tkinter, and used for the visualisation of routing.

### gui.py ###
Generates the graphical representation of a routed switch box, including calculating the positions of all the nodes and edges on a switch box and using graphics.py to draw this to the screen.

### hadlocks.py ###
Source code for the hadlocks shortest path algorithm.

### main.py ###
This file should be run in Python and used for generating tests of routing.

### routing.py ###
All routing algorithms are declared and called from this file, even if they have source code in a dedicated other file.

### simulated_annealing.py ###
Source code for simulated annealing algorithm.

### stats.py ###
Functions to calculate statistics about a routed switch box.

### switchbox.py ###
Contains the model of the switch box, made up of 'edge' and 'node' objects, and functions to connect them together to form a switch box of given size.

### testing.py ###
Functions to run single or batch tests, and also to randomly generate demands for testing.

### utils.py ###
Various other functions used within the environment.
