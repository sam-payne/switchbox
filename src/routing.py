import random

def randomWalk(sb):
    route_iterations = 0
    all_routes = []
    route_done = False
    while route_done == False:
        print("Iteration: " + str(route_iterations))
        for demand in sb.demands:
        
            curr_route = []
            curr_node = [0,0]
            src = sb.getNode(demand[0]).getID()
            dest = sb.getNode(demand[1]).getID()
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
            curr_route.append(demand[-1])
            route_iterations = route_iterations + 1
            
            all_routes.append(curr_route)

        sb_trial = sb
        route_done = True    
        if not sb_trial.checkRoutes(all_routes):
            route_done = False

        if route_done == True:
            print("Routing done after " + str(route_iterations) + " iterations")
            for r in all_routes:
                sb.addRoute(r)
                       
            
             
    
    
