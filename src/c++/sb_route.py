import subprocess
# import csv
# import sys

def sb_route(
    width=8,
    alpha=0.9,
    iterations=500,
    target=0.9,
    demand_file='',
    ):

    cmd = ['./routing']

    cmd += [
        '-w', str(width),
        '-a', str(alpha),
        '-n', str(iterations),
        '-t', str(target),
    ]

#  with open(demand_file,newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         fp
    demands = 'N3,S4'

    cmd += [demands]
    
    subprocess.call(cmd)


