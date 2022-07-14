from asyncore import read
import subprocess
import csv
import os

def getDemands(line):
    demands = []
    # print(line)
    for d in line:

        demand = list(d.split(" "))
        
        if len(demand)==2:
            demands.append(demand[0] + ',' + demand[1] + ' ')
        elif len(demand)>2:
            # Remove duplicates
            demand = list(set(demand))
            for i in range(0,len(demand)):
                for j in range(i,len(demand)):
                    if i==j:
                        continue
                    demands.append(demand[i] + ',' + demand[j] + ' ')
    # print(demands)
    return demands

     

    
def sb_route(
    width=50,
    alpha=0.9,
    iterations=500,
    target=0.8,
    demand_file='SB_database_sample.csv',
    ):
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    cmd = [os.path.join(curr_dir,'./routing')]

    cmd += [
        '-w', str(width),
        '-a', str(alpha),
        '-n', str(iterations),
        '-t', str(target),
    ]

    with open(os.path.join(curr_dir,demand_file),newline='') as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                line.pop(0)
                xcord = line.pop(0)
                ycord = line.pop(0)
                sb_name = f"sb_x{xcord}_y{ycord}_routing.txt"
                curr_cmd = cmd + ['-o',sb_name]
                demands = (getDemands(line))
                
                
                if demands:
                    subprocess.call(curr_cmd+demands)

    

    
    
    

sb_route()

