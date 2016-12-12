#!/usr/bin/python

import sys
import re
import time
import itertools
from collections import deque, OrderedDict

f = open(sys.argv[1], 'r')

initial_floors = []

equipment_pattern = re.compile('([a-z]+ generator|[a-z]+-compatible microchip)')

floorCount = 1
equipmentCount = 0
eqMap = {}

def getId(name):
    if name in eqMap:
        return eqMap[name]
    else:
        index = len(eqMap) + 1
        eqMap[name] = index
        return index

for line in f.readlines():
    equipment = equipment_pattern.findall(line)
    floor = []
    initial_floors.append(floor)
    for e in equipment:
        parts = e.split()
        equipmentCount += 1

        if parts[1] == 'generator':
            name = parts[0][0:2]
            eqId = -getId(name)
        elif parts[1] == 'microchip':
            name = parts[0][0:2]
            eqId = getId(name)
        else:
            raise Exception('Unknown equipment type "' + parts[1] + '"')

        floor.append(eqId)

    initial_floors[floorCount - 1] = sorted(initial_floors[floorCount - 1])
    floorCount += 1

print eqMap
print initial_floors


