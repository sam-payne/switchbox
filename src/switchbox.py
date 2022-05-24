

from traceback import print_tb


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

class Switchbox:
    def __init__(self,width):
        self.nodes = []
        self.demands = []
        self.used = []
        self.width = width
        for j in range(0,self.width):
            new_row = []
            for i in range(0,self.width):
                newNode = Node((i,j))
                new_row.append(newNode)
            self.nodes.append(new_row)        
       
        for row in range(0,width):
            for col in range(0,width):
                if col == 0:
                    self.nodes[row][col].connectE(self.nodes[row][col+1])
                elif col == width-1:
                    self.nodes[row][col].connectW(self.nodes[row][col-1])
                else:
                    self.nodes[row][col].connectE(self.nodes[row][col+1])
                    self.nodes[row][col].connectW(self.nodes[row][col-1])

                if row == 0:
                    self.nodes[row][col].connectS(self.nodes[row+1][col])
                elif row == width-1:
                    self.nodes[row][col].connectN(self.nodes[row-1][col])
                else:
                    self.nodes[row][col].connectN(self.nodes[row-1][col])
                    self.nodes[row][col].connectS(self.nodes[row+1][col])

       
    def getWidth(self):
        return self.width

    def setDemands(self,demands):
        for demand in demands:
            for node in demand:
                (x,y) = node
                assert ((x<self.width) and (y<self.width)), "Demands have coordinates exceeding graph width" 
                assert ((x>-1) and (y>-1)), "Demands have coordinates below zero"
        self.demands = demands

    def printDemands(self):
        print("Demands:")
        for demand in self.demands:
            print(str(demand[0]) + " <--> " + str(demand[1]))

    def printGrid(self):
        for row in range(0,self.width):
            for col in range(0,self.width):
                node = self.nodes[row][col]
                print("Node: " + str(node) + "  ",end='')
                print("Connected to " + str(node.N) + str(node.E) + str(node.S) + str(node.W) + " ",end='')
            print("")
       

problem = [[(0,0),(4,0)],[(3,4),(2,1)]]

sb = Switchbox(2)
sb.printGrid()
