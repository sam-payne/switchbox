import random
import hadlocks

# def randomWalk(sb):
#     route_iterations = 0
#     all_routes = []
#     route_done = False
#     while route_done == False:
#         print("Iteration: " + str(route_iterations))
#         for demand in sb.demands:
        
#             curr_route = []
#             curr_node = [0,0]
#             src = sb.getNode(demand[0]).getID()
#             dest = sb.getNode(demand[1]).getID()
#             curr_node[0] = src[0]
#             curr_node[1] = src[1]
#             curr_route.append(demand[0])
#             curr_route.append(src)
#             while tuple(curr_node) != dest:
#                 if (curr_node[0] == dest[0]):
#                     if dest[1]>curr_node[1]:
#                         curr_node[1] = curr_node[1] + 1
#                     else:
#                         curr_node[1] = curr_node[1] - 1
#                 elif (curr_node[1] == dest[1]):
#                     if dest[0]>curr_node[0]:
#                         curr_node[0] = curr_node[0] + 1
#                     else:
#                         curr_node[0] = curr_node[0] - 1
#                 else:       
#                     choice = random.randint(0,1)
#                     if choice==1:
#                         if dest[0]>curr_node[0]:
#                             curr_node[0] = curr_node[0] + 1
#                         else:
#                             curr_node[0] = curr_node[0] - 1
#                     else:
#                         if dest[1]>curr_node[1]:
#                             curr_node[1] = curr_node[1] + 1
#                         else:
#                             curr_node[1] = curr_node[1] - 1

#                 curr_route.append(tuple(curr_node))  
#             curr_route.append(demand[-1])
#             route_iterations = route_iterations + 1
            
#             all_routes.append(curr_route)

#         sb_trial = sb
#         route_done = True    
#         if not sb_trial.checkRoutes(all_routes):
#             route_done = False

#         if route_done == True:
#             print("Routing done after " + str(route_iterations) + " iterations")
#             for r in all_routes:
#                 sb.addRoute(r)
                       
# Always try to move horizontally until x coords matches, then move in y-direction           
# 

def Hadlocks(sb):
    used_nodes = []
    for demand in sb.demands:
        print("Routing -> ",end='')
        print(demand)
        src = sb.getNode(demand[0])
        dest = sb.getNode(demand[1])
        routeid = (src.getID(),dest.getID())
        firstNode = src.getNodeFromTerminal()
        lastNode = dest.getNodeFromTerminal()
        route = hadlocks.HadlocksAlgo(sb.width,(firstNode.getID(),lastNode.getID()),used_nodes,sb,routeid)
        used_nodes = used_nodes + route 
        route.insert(0,src.getID())
        route.append(dest.getID())
        # print(route)
        sb.addRoute(route)    
        
def HorizontalFirst(sb):
    route = []
    for demand in sb.demands:
        route = []
        curr_node = [0,0]
        src = sb.getNode(demand[0])
        dest = sb.getNode(demand[1])
        routeid = (src.getID(),dest.getID())
        firstNode = src.getNodeFromTerminal()
        lastNode = dest.getNodeFromTerminal()
        last_x, last_y = int(lastNode.getID()[0]), int(lastNode.getID()[1])
        curr_node[0] = int(firstNode.getID()[0])
        curr_node[1] = int(firstNode.getID()[1])
        route.append(src.getID())
        route.append(tuple(curr_node))
        while tuple(curr_node) != lastNode.getID():
            #print("Current node = " + str(curr_node))

            # Unless x values are the same, move horizontally first
            if curr_node[0] != last_x:
                if curr_node[0] < last_x:
                    target = (curr_node[0]+1,curr_node[1])
                else:
                    target = (curr_node[0]-1,curr_node[1])
                #print("Target = " + str(target))
                if sb.checkTurn(tuple(curr_node),tuple(target),routeid):
                    route.append((target))
                    curr_node = target
                    continue
                
            # If x values are the same, or moving horizontally fails, move vertically instead
            if curr_node[1] < last_y:
                target = (curr_node[0],curr_node[1]+1)
            elif curr_node[1] > last_y:
                target = (curr_node[0],curr_node[1]-1)
            else:
                raise Exception("Routing failed")
                
            #print("Target = " + str(target))
            # If this works, add to route, otherwise return failed
            if sb.checkTurn(tuple(curr_node),tuple(target),routeid):
                    curr_node = target
                    route.append(tuple(target))
            else:
                raise Exception("Routing failed")
        route.append(dest.getID())
        #print(route)
        sb.addRoute(route)

    
        