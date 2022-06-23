from distutils.command.config import config
from gui import drawSB
from switchbox import Switchbox
import random
from routing import *
from utils import *
from stats import *

from stats import *

########################
# Generate a single routing test for a set number of demands
def routeTestSingle(width,routing_method,routeback,common_nets,number_demands):

    demands = []
    for d in range(0,number_demands):
        # Generate the appropriate number of demands
        
        demands.append(genDemand(width,routeback,common_nets,demands))
    
    # Route using given method
    sb = Switchbox(width,demands)
    if routing_method == 'HorizontalFirst':
        HorizontalFirst(sb)

    if routing_method == 'Hadlocks':
        Hadlocks(sb)
    
    # Return switch box for further analysis
    return sb

###########################
# Run a number of tests. Run i number of tests (given by 'iterations'), using a set number of demands, increasing up to 'max_demands'
def routeTestBatch(width,routing_method, routeback, common_nets, max_demands, iterations):
    results = []
    demands = ''
    startprogress("Running batch test")

    for number_demands in range(1,max_demands+1):
        # Repeat up to the maximum number of demands to route

        success_counter = 0

        for i in range(0,iterations):
            
            # For a given number of demands, iterate a certain number of times
            demands = []
            for d in range(0,number_demands):
                # Generate the appropriate number of demands
                
                demands.append(genDemand(width,routeback,common_nets,demands))
            
            sb = Switchbox(width,demands)
            if routing_method == 'HorizontalFirst':
                try:
                    HorizontalFirst(sb)
                    #sb.printDemands()
                except:
                    print(getAllStats(sb))
                    drawSB(sb)
                    continue
                else:

                    success_counter = success_counter + 1

            if routing_method == 'Hadlocks':
                routed_success = Hadlocks(sb)
                if routed_success == len(demands):
                    success_counter = success_counter + 1   

            if routing_method == 'RandomHadlocks':
                routed_success = RandomHadlocks(sb)
                if routed_success == len(demands):
                    success_counter = success_counter + 1   
                else:
                    print(getAllStats(sb))
                    drawSB(sb)
                    break
            
            completeness = 100*((number_demands*iterations+i+1)/((max_demands+1)*iterations))         
            progress(completeness)
        results.append(success_counter)
    endprogress()
    for i,r in enumerate(results):
        percentage = round(100 * r/iterations,2)
        print("For " + str(i+1) + " demands, success -> " + str(r) + "/" + str(iterations) + " (" + str(percentage) + "%)")
    return sb

##########################################
# Generate a pair of two nodes to pass as a demand to be routed
# routeback -> whether the two nodes can be on the same side
# common_nets -> whether any two nodes in a set (prev demands passed as demands) can be the same
def genDemand(width,routeback,common_nets,demands):

    done = False
    
    while done == False:
        done = True
        d1 = 0
        d2 = 0
        d1 = genDest(width)
        d2 = genDest(width)
        if d1 == d2:
            done = False
        if routeback == False and (d1[0] == d2[0]):
            done = False
        if demands and common_nets==False:
            for prev_demand in demands:
                if (d1[0],d1[1]) in prev_demand:
                    done = False
                elif (d2[0],d2[1]) in prev_demand:
                    done = False

    demand = ((d1[0],d1[1]),(d2[0],d2[1]))
    return(demand)


#################################
# Generate a random node
def genDest(width):
    i=0
    i = random.randint(0,3)
   
    if i==0:
        pole = 'N'
    if i==1:
        pole = 'E'
    if i==2:
        pole = 'S'
    if i==3:
        pole = 'W'
    # Here the corner nodes (=0 and=W-1) and not included to avoid traps
    i = random.randint(1,width-2)
    
    return(pole,i)

