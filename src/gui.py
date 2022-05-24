from graphics import *
from switchbox import Switchbox

def drawSB(sb):
    width = sb.width
    window = 400
    buffer = window/width
    win = GraphWin("Switchbox",400,400)
    nodes = []
    # Calculate location of each node
    node_locs = []
    for i in range(0,width):
        for j in range(0,width):
            node_locs.append([int((window-buffer*2)/(width-1)*i + buffer), int((window-buffer*2)/(width-1)*j + buffer)])

    for i in range(0,width*width):
        n = Circle(Point(node_locs[i][0],node_locs[i][1]),3)
        n.draw(win)
        nodes.append(n)
    

    for demand in sb.demands:
            for n in demand:
                (x,y) = n
                nodes[x*width + y].setFill("red")

    for i in range(0,width):
        for j in range(0,width):
            # Draw 'East' edge for each node
            if i != width-1:
                l = Line(nodes[i*width + j].getCenter(),nodes[(i+1)*width + j].getCenter())    
                l.draw(win)

            if j != width-1:
                l = Line(nodes[i*width + j].getCenter(),nodes[i*width + (j+1)].getCenter())    
                l.draw(win)

    
    input("Enter to close")




