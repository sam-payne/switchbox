from graphics import *
from switchbox import Switchbox

def drawSB(sb):
    width = sb.width    
    window = 600    # GUI window dimensions (window * window)
    buffer = 50   # Size of white space around SB in window
    terminal_len = 20
    font_size = 6
    win = GraphWin("Switchbox",window,window)
    win.setBackground('white')
    nodes = []
    edges = []
    colours = ['red','blue','green','greenyellow','indigo']

    # Calculate location of each node to fit nicely in window
    for i in range(0,width):
        for j in range(0,width):
            n = Circle(Point(int((window-buffer*2)/(width-1)*i + buffer),int((window-buffer*2)/(width-1)*j + buffer)),3)
            n.draw(win)
            nodes.append(n)
    
    # Fill in source/sink nodes to be red
    col_index = 0
    for demand in sb.demands:
        col_index = col_index+1
        if col_index == len(colours):
            col_index = 0
        for n in demand:
            (x,y) = sb.getNode(n).getID()
            nodes[x*width + y].setFill(colours[col_index])

    # Draw all edges
    for i in range(0,width):
        for j in range(0,width):
            # Draw 'East' edge for each node (apart from nodes on RHS)
            if i != width-1:
                l = Line(nodes[i*width + j].getCenter(),nodes[(i+1)*width + j].getCenter())    
                l.draw(win)

            # Draw 'South' edge for each node (apart from bottom nodes)
            if j != width-1:
                l = Line(nodes[i*width + j].getCenter(),nodes[i*width + (j+1)].getCenter())    
                l.draw(win)

    # Add terminal edges and text labels
    for col in range(0,width):
        for row in range(0,width):
            if col == 0:
                x,y = nodes[col*width + row].getCenter().getX(), nodes[col*width + row].getCenter().getY()
                l = Line(Point(x,y),Point(x-terminal_len,y))
                l.draw(win)
                t = Text(Point(x-1.5*terminal_len,y),"W"+str(row))
                t.setSize(font_size)
                t.draw(win)
            if col == width-1:
                x,y = nodes[col*width + row].getCenter().getX(), nodes[col*width + row].getCenter().getY()
                l = Line(Point(x,y),Point(x+terminal_len,y))
                l.draw(win)
                t = Text(Point(x+1.5*terminal_len,y),"E"+str(row))
                t.setSize(font_size)
                t.draw(win)
            if row == 0:
                x,y = nodes[col*width + row].getCenter().getX(), nodes[col*width + row].getCenter().getY()
                l = Line(Point(x,y),Point(x,y-terminal_len))
                l.draw(win)
                t = Text(Point(x,y-1.5*terminal_len),"N"+str(col))
                t.setSize(font_size)
                t.draw(win)
            if row == width-1:
                x,y = nodes[col*width + row].getCenter().getX(), nodes[col*width + row].getCenter().getY()
                l = Line(Point(x,y),Point(x,y+terminal_len))
                l.draw(win)
                t = Text(Point(x,y+1.5*terminal_len),"S"+str(col))
                t.setSize(font_size)
                t.draw(win)
    
    # Plot routes
    col_index = 0
    for route in sb.routes:
        col_index = col_index+1
        if col_index == len(colours):
            col_index = 0
        for i in range(0,len(route)-3):
                
                x,y = sb.getNode(route[i+1]).getID()
                src = nodes[int(x)*width + int(y)].getCenter()
                x,y = sb.getNode(route[int(i)+2]).getID()
                dest = nodes[int(x)*width + int(y)].getCenter()
                l = Line(src,dest)
                l.setFill(colours[col_index])
                l.draw(win)

    win.getMouse()
    win.close()



