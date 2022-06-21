#Q-negative - further away from dest (return only unvisited)
def getQNegativeNeighbours(node, dest, width, visited):
    neighbours_temp = []
    neighbours = []
    x_node = node[0]
    y_node = node[1]
    x_dest = dest[0]
    y_dest = dest[1]

    if x_dest > x_node:
        if x_node-1 >= 0:
            neighbours_temp.append((x_node-1,y_node))
    elif x_node > x_dest:
        if x_node+1 <= width-1:
            neighbours_temp.append((x_node+1,y_node))

    if y_dest > y_node:
        if y_node-1 >= 0:
            neighbours_temp.append((x_node,y_node-1))
    elif y_node > y_dest:
        if y_node+1 <= width-1:
            neighbours_temp.append((x_node,y_node+1))

    for n in neighbours_temp:
        if n not in visited:
            neighbours.append(n)

    return neighbours

#Q-positive - closer to dest (return only unvisited)
def getQPositiveNeighbours(node, dest, width, visited):
    neighbours = []
    neighbours_temp = []
    x_node = node[0]
    y_node = node[1]
    x_dest = dest[0]
    y_dest = dest[1]

    if x_dest > x_node:
        neighbours_temp.append((x_node+1,y_node))
    elif x_node > x_dest:
        neighbours_temp.append((x_node-1,y_node))

    if y_dest > y_node:
        neighbours_temp.append((x_node,y_node+1))
    elif y_node > y_dest:
        neighbours_temp.append((x_node,y_node-1))

    for n in neighbours_temp:
        if n not in visited:
            neighbours.append(n)

    return neighbours

def HadlocksAlgo(width,demands):
    demands = [((2,2),(7,4))]
    visited = []
    p_stack = []
    n_stack = []
    width = 0
    for demand in demands:
        src = demand[0]
        dest = demand[1]
        d = 0
        u_node = src
        while u_node != dest:
            visited.append(u_node)
            for qneg in getQNegativeNeighbours(u_node,dest,width):
                n_stack.append(qneg)
            
            if not getQPositiveNeighbours(u_node,dest,width):
                if not p_stack:
                    if not n_stack:
                        raise Exception("No path exists")
            



HadlocksAlgo(8,None)