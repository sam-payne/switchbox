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

---

## Usage ##

To run a single switch box routing test for a given width and number of demands, use the 'routeTestSingle' function. This returns a switch box object, which can be passed to the drawSB(sb) function to generate a graphic, or getFullReport(sb) to return a string of the statistics report.
Example:
- `sb = routeTestSingle(width=8,routing_method='RandomHadlocks',routeback=True,common_nets=False,number_demands=8,corners=True)`
- `drawSB(sb)`
- `print(getFullReport(sb))`

To run a batch test, which runs multiple iterations of routing trials for increasing numbers of demands, use routeTestBatch():
- `routeTestBatch(16,"SimulatedAnnealing",routeback=True,common_nets=False,max_demands=28,iterations=15,corners=True)`

Or, you can route your own specified demands manually, defined in a file called "demands.txt" (see example file):
- `demands = parseDemands("demands.txt")`
- `sb = Switchbox(10,demands)`    *Create a switchbox object with a width of 10, and demands from the file*
- `RandomHadlocks(sb)`      *Pass switch box object to routing function*
- `drawSB(sb)`
