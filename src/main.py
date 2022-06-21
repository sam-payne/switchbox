from switchbox import Switchbox
from gui import *
from utils import *
from routing import *
from testing import getRouteEfficiency, routeTestSingle, routeTestBatch

# demands = parseDemands("demands.txt")

# sb = Switchbox(12,demands)
# sb.printDemands()

# Hadlocks(sb)
# getRouteEfficiency(sb)
# drawSB(sb)       

routeTestSingle(32,"Hadlocks",False,False,15)
