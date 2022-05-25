class Node:
    def __init__(self,coord):
        self.coord = coord
        self.N = None
        self.E = None
        self.S = None
        self.W = None
    
    def connectN(self,node):
        self.N = node
    
    def connectE(self,node):
        self.E = node

    def connectS(self,node):
        self.S = node

    def connectW(self,node):
        self.W = node

    def __str__(self):
        return str(self.coord)

    def __repr__(self):
        return str(self.coord)

class Terminal:
    def __init__(self,id):
        self.id = id
        self.side = id[0]
        self.node = None
    
    # Connect up terminal to node (and node to terminal)
    def connect(self,node):
        self.node = node
        print("Connected " + str(self) + " to " + str(node))
        if self.side == 'N':
            node.connectN(self)
        elif self.side == 'E':
            node.connectE(self)
        elif self.side == 'S':
            node.connectS(self)
        elif self.side == 'W':
            node.connectW(self)

    def __str__(self):
        return str(self.id[0])+str(self.id[1])

    def __repr__(self):
        return str(self.id[0])+str(self.id[1])

class Switchbox:
    def __init__(self,width):
        self.nodes = []
        self.terminals = []
        self.demands = []
        self.used = []
        self.width = width
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
                print("Connected to " + str(node.N) + str(node.E) + str(node.S) + str(node.W))
            print("")
       
    def getTerminal(self,id):
        for t in self.terminals:
            if t.id == id:
                return t

