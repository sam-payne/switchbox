from utils import *

class Node:
    def __init__(self,id):
        self.id = id
        self.N = None
        self.E = None
        self.S = None
        self.W = None
        self.config = []
        self.routedNodes = [(None,None)]
    
    def connectN(self,node):
        self.N = node
    
    def connectE(self,node):
        self.E = node

    def connectS(self,node):
        self.S = node

    def connectW(self,node):
        self.W = node

    def getID(self):
        return self.id

    # Return relative direction of a neighbour node
    def getDir(self,id):
        
        if self.N.id == id:
            return 'N'
        if self.E.id == id:
            return 'E'
        if self.S.id == id:
            return 'S'
        if self.W.id == id:
            return 'W'
        raise Exception("Cannot reach node " + str(id)) # Cannot make the required connection

    # Calc switch config for a given in/out direction
    def route(self,src,dest,routeid):
        for route in self.routedNodes:
            
            #If either src or dest of the route IDs match - part of the same mesh so OK to share an edge
            if route[0] == src and not compareRouteID(route[1],routeid):
                raise Exception("Route conflict between {Route:" + str(routeid) + "} and {Route" + str(route[1]))
            if route[0] == dest and not compareRouteID(route[1],routeid):
                raise Exception("Route conflict between {  Route:" + str(routeid) + "  } and {  Route" + str(route[1]) + "  }")
        src_dir = self.getDir(src)
        dest_dir = self.getDir(dest)
        
        self.routedNodes.append((src,routeid))
        self.routedNodes.append((dest,routeid))
        self.config.append((src_dir,dest_dir))

    def printConfig(self):
        if len(self.config) == 0:
            return "Unconnected"
        else:
            return str(self.config)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.id

class Terminal:
    def __init__(self,id):
        self.id = id
        self.side = id[0]
        self.node = None
    
    # Connect up terminal to node (and node to terminal)
    def connect(self,node):
        self.node = node
        # print("Connected " + str(self) + " to " + str(node))
        if self.side == 'N':
            node.connectN(self)
        elif self.side == 'E':
            node.connectE(self)
        elif self.side == 'S':
            node.connectS(self)
        elif self.side == 'W':
            node.connectW(self)

    def getID(self):
        return self.id

    def __str__(self):
        return str(self.id[0])+str(self.id[1])

    def __repr__(self):
        return str(self.id[0])+str(self.id[1])

class Switchbox:
    def __init__(self,width,demands):
        self.nodes = []
        self.terminals = []
        self.edges = []
        self.demands = []
        self.used = []
        self.routes = []
        self.width = width

        # Check demands and set
        self.setDemands(demands)

        # Create nodes and append to self.nodes list
        for i in range(0,self.width):
            new_col = []
            for j in range(0,self.width):
                newNode = Node((i,j))
                new_col.append(newNode)
            self.nodes.append(new_col)        
        

       # Create terminals - give them an ID tuple and connect them to the appropriate edge node
        for x in range(0,self.width):
            id = ('N',x)
            t = Terminal(id)
            t.connect(self.nodes[x][0])
            self.terminals.append(t)

            id = ('E',x)
            t = Terminal(id)
            t.connect(self.nodes[width-1][x])
            self.terminals.append(t)

            id = ('S',x)
            t = Terminal(id)
            t.connect(self.nodes[x][width-1])
            self.terminals.append(t)

            id = ('W',x)
            t = Terminal(id)
            t.connect(self.nodes[0][x])
            self.terminals.append(t)

        # Connect up nodes to each other    
        for col in range(0,width):
            for row in range(0,width):
                if col == 0:
                    self.nodes[col][row].connectE(self.nodes[col+1][row])
                elif col == width-1:
                    self.nodes[col][row].connectW(self.nodes[col-1][row])
                else:
                    self.nodes[col][row].connectE(self.nodes[col+1][row])
                    self.nodes[col][row].connectW(self.nodes[col-1][row])

                if row == 0:
                    self.nodes[col][row].connectS(self.nodes[col][row+1])
                elif row == width-1:
                    self.nodes[col][row].connectN(self.nodes[col][row-1])
                else:
                    self.nodes[col][row].connectN(self.nodes[col][row+1])
                    self.nodes[col][row].connectS(self.nodes[col][row-1])

        
    def getWidth(self):
        return self.width

    def setDemands(self,demands):
        for demand in demands:
            for node in demand:
                (side,val) = node
                assert (side=='N') or (side=='W') or (side=='S') or (side=='E'), "Invalid demand for node " + str(node) 
                assert (val>-1) and (val<self.width), "Invalid demand for node " + str(node)       
        self.demands = demands

    def printDemands(self):
        print("Demands:")
        for demand in self.demands:
            print(str(demand[0]) + " <--> " + str(demand[1]))

    def printConnections(self):
        for col in range(0,self.width):
            for row in range(0,self.width):
                node = self.nodes[col][row]
                print("Node: " + str(node) + "  ",end='')
                print("Connected to " + str(node.N) + str(node.E) + str(node.S) + str(node.W),end='')
                print(" - Config: " + node.printConfig())
            print("")
       
    def getNode(self,id):
        # If ID is a terminal, then get adjacent node
        for t in self.terminals:
            if t.getID() == id:
                return t.node
        for col in self.nodes:
            for n in col:
                if n.getID() == id:
                    return n

    def addRoutes(self,routes):
        # Takes a route between two terminals, works out node config, adds this to the Sb and removes used edges
        for route in routes:
            self.routes.append(route)
            routeid = (route[0],route[-1])
            src = route[0]
            dest = route[-1]
            print(route)
            assert (src[0] == 'N') or (src[0] == 'E') or (src[0] == 'S') or (src[0] == 'W'), "Route does not start at a terminal"
            assert (dest[0] == 'N') or (dest[0] == 'E') or (dest[0] == 'S') or (dest[0] == 'W'), "Route does not finish at a terminal"
            for i in range(0,len(route)-2):
                curr = self.getNode(route[i+1])
                print("curr = " + str(curr.getID()))
                # print("curr[0" + str(self.getNode(route[i]).getID()))
                curr.route(route[i],route[i+2],routeid)

