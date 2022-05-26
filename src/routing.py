import random

def randomWalk(sb):
    routes = []
    for demand in sb.demands:
        curr_route = []
        curr_node = [0,0]
        src = sb.getNode(demand[0]).getID()
        dest = sb.getNode(demand[1]).getID()
        print(src)
        print(dest)
        curr_node[0] = src[0]
        curr_node[1] = src[1]
        curr_route.append(demand[0])
        curr_route.append(src)
        while tuple(curr_node) != dest:
            if (curr_node[0] == dest[0]):
                if dest[1]>curr_node[1]:
                    curr_node[1] = curr_node[1] + 1
                else:
                    curr_node[1] = curr_node[1] - 1
            elif (curr_node[1] == dest[1]):
                if dest[0]>curr_node[0]:
                    curr_node[0] = curr_node[0] + 1
                else:
                    curr_node[0] = curr_node[0] - 1
            else:       
                choice = random.randint(0,1)
                if choice==1:
                    if dest[0]>curr_node[0]:
                        curr_node[0] = curr_node[0] + 1
                    else:
                        curr_node[0] = curr_node[0] - 1
                else:
                    if dest[1]>curr_node[1]:
                        curr_node[1] = curr_node[1] + 1
                    else:
                        curr_node[1] = curr_node[1] - 1

            curr_route.append(tuple(curr_node))  
        routes.append(curr_route)
        curr_route.append(demand[-1])
    print(routes)
    return routes
