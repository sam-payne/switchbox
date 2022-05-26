

def manhat(a,b):
    # Return manhattan distance between two coordinates
    ax, ay = a
    bx, by = b
    if ax > bx:
        diffx = ax - bx
    else:
        diffx = bx - ax
    if ay > by:
        diffy = ay - by
    else:
        diffy = by - ay
    return diffx + diffy

def compareRouteID(id1,id2):
    if id1[0] == id2[0] or id1[0] == id2[1]:
        return True
    elif id1[1] == id2[0] or id1[1] == id2[1]:
        return True
    else:
        return False

def parseDemands(input_file):
    demands = []
    with open(input_file,"r") as demand_file:
        for line in demand_file:
            line = line.split(',')
            src = line[0]
            dest = line[1]
            demand = ((src[0],int(src[1])),(dest[0],int(dest[1])))
            demands.append(demand)
    return demands