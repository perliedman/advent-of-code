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
for line in f.readlines():
    equipment = equipment_pattern.findall(line)
    floor = OrderedDict()
    initial_floors.append(floor)
    for e in equipment:
        parts = e.split()
        if parts[1] == 'generator':
            eqId = parts[0][0:2].capitalize() + 'G'
        elif parts[1] == 'microchip':
            eqId = parts[0].split('-')[0][0:2].capitalize() + 'M'
        else:
            raise Exception('Unknown equipment type "' + parts[1] + '"')

        floor[eqId] = True
        equipmentCount += 1

    floorCount += 1

def printFloors(floors, elevatorFloor):
    for i in xrange(4, 0, -1):
        f = floors[i - 1]
        print '* ' if i == elevatorFloor else '  ', i, ' '.join(f)

def isValid(floors, f, t):
    for i in range(min(f, t), max(f, t) + 1):
        gens = [eqId for eqId in floors[i - 1] if eqId.endswith('G')]
        if len(gens):
            for c in [eqId for eqId in floors[i - 1] if eqId.endswith('M')]:
                if not (c[0:2] + 'G') in floors[i - 1]:
                    #raise Exception('%s on floor %d: %s' % (c, i - 1, ', '.join(floors[i - 1])))
                    return False
    return True

def createFloors(floors, equipment, fromFloor, toFloor):
    newFloors = []
    for f in floors:
        newFloors.append(OrderedDict(f))
    for eqId in equipment:
        del newFloors[fromFloor - 1][eqId]
        newFloors[toFloor - 1][eqId] = True

    return newFloors

def possibleMoves(floor):
    equipment = floor.keys()
    one = [[eqId] for eqId in equipment]
    two = list(itertools.combinations(equipment, 2))

    pairs = [(p1,p2) for (p1, p2) in two if p1[0:2] == p2[0:2]]
    for p in pairs[1:]:
        two.remove(p)

    return one + two

def moveId(move, f, t):
    return ''.join(move) + ';' + str(f) + ';' + str(t)

def play(elevatorFloor, floors):
    examinedMoves = 0

    queue = deque()
    queue.append((elevatorFloor, floors, []))

    states = set()
    ignored = 0

    while len(queue):
        (elevatorFloor, floors, moves) = queue.popleft()
        floorI = elevatorFloor - 1

        examinedMoves += 1
        if examinedMoves % 10000 == 0:
            print examinedMoves, 'moves examined at depth', len(moves), ',', len(states), 'seen states,', ignored, 'dupes ignored states'

        candFloors = [f for f in [elevatorFloor + 1, elevatorFloor - 1] if f > 0 and f < 5]
        possible = possibleMoves(floors[floorI])
        for nextFloor in candFloors:
            for move in possible:
                newFloors = createFloors(floors, move, elevatorFloor, nextFloor)
                if len(newFloors[3]) == equipmentCount:
                    print len(states), 'seen states,', examinedMoves, 'moves examined'
                    return moves + [move]
                else:
                    h = str(nextFloor) + ';' + ';'.join([','.join(f) for f in newFloors])
                    if not h in states:
                        if isValid(floors, elevatorFloor, nextFloor):
                            states.add(h)
                            queue.append((nextFloor, newFloors, moves + [moveId(move, elevatorFloor, nextFloor)]))
                    else:
                        ignored += 1
    
    print len(states), 'seen states,', examinedMoves, 'moves examined'
    return None

best = play(1, initial_floors)

if best:
    print best
    print len(best)
else:
    print 'No solution found :('

#printFloors(createFloors(floors, ['HyM', 'LiM'], 1, 2), 2)
#print possibleMoves(floors[0])