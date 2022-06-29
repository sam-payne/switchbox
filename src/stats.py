from utils import *
from switchbox import Switchbox


def getRouteEfficiency(sb):
    report = "\n\n******** Routing Efficiency ********\n"
    report += "(The length of each route compared to its shortest possible path (Manhatten distance))\n\n"
    if not sb.routes:
        return 1
    total_len = 0
    total_man = 0
    for r in sb.routes:
        length = len(r) - 3
        total_len = total_len + length
        manhatten = manhat(r[1],r[-2])
        total_man = total_man + manhatten
        id = str(r[0]) + "<->" + str(r[-1])
        percent = round(100*(manhatten/length),2)
        report += "For route " + id + ", length = " + str(length) + " compared to possible " + str(manhatten) + " (" + str(percent) + "%)\n"
    overall_percent = round(100*total_man/total_len,2)
    report += ("\nOverall Efficiency = " + str(overall_percent) + "%\n")
    report += "********************************\n\n"
    return report

def getRoutingSuccess(sb):
    success_counter = 0
    demand_satisfied = False
    fails = ""
    report = "\n\n******** Routing Summary ********\n"
    for d in sb.demands:
        demand_satisfied = False
        for r in sb.routes:
            if d[0]==r[0] and d[-1]==r[-1]:
                demand_satisfied = True
                success_counter += 1
                report += "Successfully routed " + str(d[0]) + " <-> " + str(d[1]) + "\n"
        if demand_satisfied == False:
            fails += "Failed to route " + str(d[0]) + " <-> " + str(d[1]) + "\n"

    report += "\n" + fails
    report += "\nRouted " + str(len(sb.routes)) + "/" + str(len(sb.demands)) + " (" + str(round(100*len(sb.routes)/len(sb.demands),2)) + "%)\n\n"
    if len(sb.routes) == len(sb.demands):
        report += "******** Routing successful! ********"
    else:
        report += "******** Routing failed! ********"
    return report

def getSBUtilisation(sb):
    
    unused = 0
    single_config = 0
    double_config = 0
    no_sbs = sb.width * sb.width
    for row in sb.nodes:
        for n in row:
            if not n.config:
                unused = unused + 1
            elif len(n.config) == 1:
                single_config = single_config+1
            elif len(n.config) == 2:
                double_config = double_config+1
    report = "\n\n********* Switch Box Utilisation ********\n\n"
    report += str(unused) + "/" + str(no_sbs) + " unused (" + str(round(100*unused/no_sbs,2)) + "%)\n"
    report += str(single_config) + "/" + str(no_sbs) + " with one signal passing through (" + str(round(100*single_config/no_sbs,2)) + "%)\n"
    report += str(double_config) + "/" + str(no_sbs) + " with two signals passing through (" + str(round(100*double_config/no_sbs,2)) + "%)\n"
    report += "************************"
    return report

def getFullReport(sb):
    report = "******** Routing finished - full report... ********"
    report += getSBUtilisation(sb)
    report += getRouteEfficiency(sb)
    report += getRoutingSuccess(sb)
    return report