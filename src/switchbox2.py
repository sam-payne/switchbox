from utils import *

class Node:
    def __init__(self,id,isTerminal):
        self.id = id
        self.N = None
        self.E = None
        self.S = None
        self.W = None
        self.isTerminal = isTerminal
        self.config = []
        self.routedNodes = [(None,None)]

    def getX(self):
        return int(self.id[0])    

    def getY(self):
        return int(self.id[1])

    def printConfig(self):
        if len(self.config) == 0:
            return "Unconnected"
        else:
            return str(self.config)


    def route(self,src_node,dest_node,routeid):
        # Determine which outgoing edge is required
        if self.N != None:
            if self.N.getOtherNode(self).getID() == dest_node:
                edge = self.N
        if self.E != None:
            if self.E.getOtherNode(self).getID() == dest_node:
                edge = self.E
        if self.S != None:
            if self.S.getOtherNode(self).getID() == dest_node:
                edge = self.S
        if self.W != None:
            if self.W.getOtherNode(self).getID() == dest_node:
                edge = self.W
        
        if edge.netName == None:
            edge.netName = routeid
        elif edge.netName != routeid:
            raise Exception("Route conflict")
        
        src_dir = self.getDir(src_node)
        dest_dir = self.getDir(dest_node)
        self.config.append((src_dir,dest_dir))
        
    def getDir(self,id):
        
        if self.N.getOtherNode(self).getID() == id:
            return 'N'
        if self.E.getOtherNode(self).getID() == id:
            return 'E'
        if self.S.getOtherNode(self).getID() == id:
            return 'S'
        if self.W.getOtherNode(self).getID() == id:
            return 'W'

    def getID(self):
        return self.id
    
    def getEdge(self,dir):
        if dir=='N':
            return self.N
        elif dir=='E':
            return self.E
        elif dir=='S':
            return self.S
        elif dir=='W':
            return self.W
        else:
            raise Exception("Invalid dirs")

    def addEdge(self,edge,dir):
        if dir=='N':
            edge.connectNode(self)
            self.N = edge
        elif dir=='E':
            edge.connectNode(self)
            self.E = edge
        elif dir=='S':
            edge.connectNode(self)
            self.S = edge
        elif dir=='W':
            edge.connectNode(self)
            self.W = edge
        else:
            raise Exception("Invalid dirs")

    def getNodeFromTerminal(self):
        # If terminal, then get attached node
        if self.N != None:
            return self.N.getOtherNode(self)
        elif self.E != None:
            return self.E.getOtherNode(self)
        elif self.S != None:
            return self.S.getOtherNode(self)
        elif self.W != None:
            return self.W.getOtherNode(self)
        else:
            raise Exception("No node attached to terminal")  

class Edge:
    def __init__(self,id):
        self.node1 = None #Node 1 is the primary node - edge is always South or East of Node 1
        self.node2 = None
        self.netName = None
        self.id = id

    def getID(self):
        return self.id

    def connectNode(self,node):
        if self.node1 == None:
            self.node1 = node
        elif self.node2 == None:
            self.node2 = node
        else:
            raise Exception("More than two nodes connected to edge (ID:"+str(self.id)+")!")

    def getOtherNode(self,curr_node):
        if self.node1 == curr_node:
            return self.node2
        elif self.node2 == curr_node:
            return self.node1
        else:
            raise Exception("Invalid node")
        
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
                newNode = Node((i,j),False)
                new_col.append(newNode)
            self.nodes.append(new_col)        
        
        # Connect all nodes together via an edge
        for col in range(0,width):
            for row in range(0,width):
                if col == 0:
                    self.connectTwoNodes(self.nodes[col][row],'E',self.nodes[col+1][row],'W')
                elif col == width-1:
                    self.connectTwoNodes(self.nodes[col-1][row],'E',self.nodes[col][row],'W')
                else:
                    self.connectTwoNodes(self.nodes[col][row],'E',self.nodes[col+1][row],'W')
                    self.connectTwoNodes(self.nodes[col-1][row],'E',self.nodes[col][row],'W')

                if row == 0:
                    self.connectTwoNodes(self.nodes[col][row],'S',self.nodes[col][row+1],'N')
                elif row == width-1:
                    self.connectTwoNodes(self.nodes[col][row-1],'S',self.nodes[col][row],'N')
                else:
                    self.connectTwoNodes(self.nodes[col][row],'S',self.nodes[col][row+1],'N')
                    self.connectTwoNodes(self.nodes[col][row-1],'S',self.nodes[col][row],'N')


        # Create terminals - give them an ID tuple and connect them to the appropriate node via an edge
        for x in range(0,self.width):
            id = ('N',x)
            t = Node(id,True)
            self.connectTwoNodes(t,'S',self.nodes[x][0],'N')
            self.terminals.append(t)

            id = ('E',x)
            t = Node(id,True)
            self.connectTwoNodes(t,'W',self.nodes[width-1][x],'E')
            self.terminals.append(t)

            id = ('S',x)
            t = Node(id,True)
            self.connectTwoNodes(t,'N',self.nodes[x][width-1],'S')
            self.terminals.append(t)

            id = ('W',x)
            t = Node(id,True)
            self.connectTwoNodes(t,'E',self.nodes[0][x],'W')
            self.terminals.append(t)
  

    def connectTwoNodes(self,node1,node1_dir,node2,node2_dir):
        if (node1_dir == 'E') or (node1_dir == 'S'):
            edgeid = str(node1.getID()) + "-" + node1_dir
        elif (node2_dir == 'E') or (node2_dir == 'S'):
            edgeid = str(node2.getID()) + "-" + node2_dir


        if node1.getEdge(node1_dir) == None:
            if node2.getEdge(node2_dir) == None:
                # No edge exists so create one
                edge = Edge(edgeid)
                self.edges.append(edge)
                node1.addEdge(edge,node1_dir)
                node2.addEdge(edge,node2_dir)
            else:
                edge = node2.getEdge(node2_dir)
                node1.addEdge(edge,node1_dir)
        else:
            if node2.getEdge(node2_dir) == None:
                # No edge exists so create one
                edge = node1.getEdge(node1_dir)
                node2.addEdge(edge,node2_dir)
            
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
                print("Connected to " + str(node.N.getOtherNode().getID()) + str(node.E.getOtherNode().getID()) + str(node.S.getOtherNode().getID()) + str(node.W.getOtherNode().getID()),end='')
                print(" - Config: " + node.printConfig())
            print("")

    def printEdges(self):
        dirs = ['N','E','S','W']
        for col in self.nodes:
            for n in col:
                print("Node: " + str(n.getID()) + " -> ",end='')
                for dir in dirs:
                    if n.getEdge(dir) != None:
                        print(str(n.getEdge(dir).getID()) + " ",end='')
        print("Terminals: ")
        for t in self.terminals:
            print("Node: " + str(t.getID()) + " -> ",end='')
            for dir in dirs:
                if t.getEdge(dir) != None:
                    print(str(t.getEdge(dir).getID()) + " ",end='')

    def getNodesOfEdge(self,edgeid):
        for e in self.edges:
            if e.getID() == edgeid:
                print("For edge" + str(e.getID()) + " -> Node1: = " + str(e.node1.getID()) + " Node2: " + str(e.node2.getID()))

    def getNode(self,nodeid):
        for t in self.terminals:
            if t.getID() == nodeid:
                return t
        for col in self.nodes:
            for n in col:
                if (n.getID()) == nodeid:
                    return n

    def addRoute(self,route):
        # Takes a route between two terminals, works out node config, adds this to the Sb and removes used edges
        
        self.routes.append(route)
        routeid = (route[0],route[-1])
        src = route[0]
        dest = route[-1]

        assert (src[0] == 'N') or (src[0] == 'E') or (src[0] == 'S') or (src[0] == 'W'), "Route does not start at a terminal"
        assert (dest[0] == 'N') or (dest[0] == 'E') or (dest[0] == 'S') or (dest[0] == 'W'), "Route does not finish at a terminal"
        for i in range(0,len(route)-2):
            curr = self.getNode(route[i+1])
            curr.route(route[i],route[i+2],routeid)

    def checkRoute(self,route):
        routeid = (route[0],route[-1])
        src = route[0]
        dest = route[-1]
        assert (src[0] == 'N') or (src[0] == 'E') or (src[0] == 'S') or (src[0] == 'W'), "Route does not start at a terminal"
        assert (dest[0] == 'N') or (dest[0] == 'E') or (dest[0] == 'S') or (dest[0] == 'W'), "Route does not finish at a terminal"
        
        for i in range(0,len(route)-2):
            curr = self.getNode(route[i+1])
            try: 
                curr.route(route[i],route[i+2],routeid)
            except:
                return False
        return True
