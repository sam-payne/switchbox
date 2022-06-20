from gui2 import drawSB
from switchbox2 import Switchbox
import random
from routing import *

def routeTest(width,routing_method, routeback, nets, iterations, max_demands):
    results = []
    demands = ''
    for number_demands in range(1,max_demands+1):
        # Repeat up to the maximum number of demands to route

        success_counter = 0

        for i in range(0,iterations):
            # For a given number of demands, iterate a certain number of times
            demands = []
            for d in range(0,number_demands):
                # Generate the appropriate number of demands
                
                demands.append(genDemand(width,routeback))
            
            sb = Switchbox(width,demands)
            if routing_method == 'HorizontalFirst':
                try:
                    HorizontalFirst(sb)
                    #sb.printDemands()
                except:
                    continue
                else:
                    success_counter = success_counter + 1
                    # if number_demands == max_demands:
                    #     drawSB(sb)
                    #     break
    
        results.append(success_counter)

    for i,r in enumerate(results):
        percentage = 100 * r/iterations
        print("For " + str(i+1) + " demands, success -> " + str(r) + "/" + str(iterations) + " (" + str(percentage) + "%)")

def genDemand(width,routeback):
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
    demand = ((d1[0],d1[1]),(d2[0],d2[1]))
    return(demand)


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
    i = random.randint(0,width-1)
    
    return(pole,i)

routeTest(8,"HorizontalFirst",routeback=False,nets=False,iterations=1000,max_demands=10)