
import subprocess
import csv
import os
#########################################
WIDTH=50                                # Switch box width
ALPHA=0.95                              # Alpha parameter (default 0.95)    
ITERATIONS=500                          # Max number of iterations of annealing algoritm
TARGET=0.9                              # Algorithm will return when all paths routed AND total length < (optimal length / target)
DEMAND_FILE='SB_database_sample.csv'    # File path for demands csv
#########################################


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
    width,
    alpha,
    iterations,
    target,
    demand_file,
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
            sb_name = "sb_out.txt"
            sb_name = os.path.join(curr_dir,sb_name)
            f = open(sb_name,"w")
            f.close()
            curr_cmd = cmd + ['-o',sb_name]
            for line in reader:
                line.pop(0)
                xcord = line.pop(0)
                ycord = line.pop(0)
                id = str(xcord + ',' + ycord)
                curr_cmd = cmd + ['-i',id]

                # sb_name = f"sb_x{xcord}_y{ycord}_routing.csv"
                # sb_name = "sb_out.txt"
                # sb_name = os.path.join(curr_dir,sb_name)
                # curr_cmd = cmd + ['-o',sb_name]

                demands = (getDemands(line))           
                
                if demands:
                    print(f"\nRouting SB_x{xcord}_y{ycord}...\n")
                    subprocess.run(curr_cmd+demands)

if __name__ == "__main__":
    sb_route(width=WIDTH,alpha=ALPHA,iterations=ITERATIONS,target=TARGET,demand_file=DEMAND_FILE)  

