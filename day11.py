#!/usr/bin/python

import sys
import re
import itertools
import heapq

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

def correct(floor):
    gens = [c for c in floor if c < 0]
    chipsWoGen = [c for c in floor if c > 0 and not -c in floor]
    return len(gens) == 0 or len(chipsWoGen) == 0

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

    initial_floors[floorCount - 1] = tuple(sorted(initial_floors[floorCount - 1]))
    floorCount += 1

print eqMap
print initial_floors

initial = (0, tuple(initial_floors))

q = []
heapq.heappush(q, (0, initial))
costs = {
    initial: 0
}

while q:
    _, current = heapq.heappop(q)

    (elevator, floors) = current

    if len(floors[3]) == equipmentCount:
        break

    possibleMoves = [(x,) for x in floors[elevator]] + list(itertools.combinations(floors[elevator], 2))
    newCost = costs[current] + 1

    for nextFloor in [f for f in [elevator + 1, elevator - 1] if f >= 0 and f <= 3]:
        for m in possibleMoves:
            nextFloors = list(floors)
            nextFloors[nextFloor] = tuple(sorted(floors[nextFloor] + m))
            nextFloors[elevator] = tuple([eqId for eqId in floors[elevator] if eqId not in m])

            if correct(nextFloors[nextFloor]) and correct(nextFloors[elevator]):
                nextState = (nextFloor, tuple(nextFloors))
                if nextState not in costs or newCost < costs[nextState]:
                    heapq.heappush(q, (newCost - len(nextFloors[3]) * 3, nextState))
                    costs[nextState] = newCost

print costs[current]
