from switchbox import Switchbox
from gui import *
from utils import *
from routing import *

demands = parseDemands("demands.txt")

sb = Switchbox(12,demands)
sb.printDemands()

randomWalk(sb)
drawSB(sb)                                                                                                    