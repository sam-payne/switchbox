from switchbox import Switchbox
from gui import *
from utils import *
from routing import *

demands = parseDemands("demands.txt")

sb = Switchbox(9,demands)
sb.printDemands()

Hadlocks(sb)
drawSB(sb)                                                                                                    