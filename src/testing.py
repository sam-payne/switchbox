from gui import drawSB
from switchbox import Switchbox
import random
from routing import *
from utils import *

def routeTestSingle(width,routing_method,routeback,nets,number_demands):

    demands = []
    for d in range(0,number_demands):
        # Generate the appropriate number of demands
        
        demands.append(genDemand(width,routeback))
    
    sb = Switchbox(width,demands)
    if routing_method == 'HorizontalFirst':
        HorizontalFirst(sb)

    if routing_method == 'Hadlocks':
        Hadlocks(sb)
    
    getRouteEfficiency(sb)
   # drawSB(sb)

def routeTestBatch(width,routing_method, routeback, nets, iterations, max_demands):
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
                    drawSB(sb)
                    continue
                else:
                    success_counter = success_counter + 1

            if routing_method == 'Hadlocks':
                try:
                    Hadlocks(sb)
                    #sb.printDemands()
                except:
                    #drawSB(sb)
                    continue
                else:
                    success_counter = success_counter + 1   
    
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
    i = random.randint(1,width-2)
    
    return(pole,i)

def getRouteEfficiency(sb):
    if not sb.routes:
        return 1
    total_len = 0
    total_man = 0
    for r in sb.routes:
        length = len(r) - 3
        total_len = total_len + length
        manhatten = manhat(r[1],r[-2])
        total_man = total_man + manhatten
        id = str(r[0]) + str(r[-1])
        percent = 100*(manhatten/length)
        print("For route " + id + ", length = " + str(length) + " compared to possible " + str(manhatten) + " (" + str(percent) + "%)")
    overall_percent = 100*total_man/total_len
    print("Overall Efficiency = " + str(overall_percent) + "%")
