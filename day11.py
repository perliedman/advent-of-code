#!/usr/bin/python

import sys
import re
import time
import itertools
from collections import deque

f = open(sys.argv[1], 'r')

initial_floors = []

equipment_pattern = re.compile('([a-z]+ generator|[a-z]+-compatible microchip)')

floorCount = 1
equipmentCount = 0
for line in f.readlines():
    equipment = equipment_pattern.findall(line)
    floor = []
    initial_floors.append(floor)
    for e in equipment:
        parts = e.split()
        if parts[1] == 'generator':
            eqId = parts[0][0:2].capitalize() + 'G'
        elif parts[1] == 'microchip':
            eqId = parts[0].split('-')[0][0:2].capitalize() + 'M'
        else:
            raise Exception('Unknown equipment type "' + parts[1] + '"')

        floor.append(eqId)
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
        newFloors.append(f[:])
    newFloors[fromFloor - 1] = [eqId for eqId in floors[fromFloor - 1] if not eqId in equipment]
    newFloors[toFloor - 1] += equipment

    return newFloors

def possibleMoves(floor):
    one = [[eqId] for eqId in floor]
    two = list(itertools.combinations(floor, 2))
    return one + two

def moveId(move, f, t):
    return ''.join(move) + ';' + str(f) + ';' + str(t)

def play(elevatorFloor, floors):
    examinedMoves = 0

    queue = deque()
    queue.append((elevatorFloor, floors, []))

    while len(queue):
        (elevatorFloor, floors, moves) = queue.popleft()
        floorI = elevatorFloor - 1

        examinedMoves += 1
        if (examinedMoves % 10000 == 0):
            print examinedMoves, ' moves examined at depth ', len(moves)

        candFloors = [f for f in [elevatorFloor + 1, elevatorFloor - 1] if f > 0 and f < 5]
        for nextFloor in candFloors:
            possible = possibleMoves(floors[floorI])
            filteredPossible = [m for m in possible if not moveId(m, elevatorFloor, nextFloor) in moves]
#            if len(filteredPossible) == 0:
#                print 'No possible moves at ', len(moves)
    #        if len(possible) != len(filteredPossible):
    #            print 'Removed ', len(possible) - len(filteredPossible)
            for move in filteredPossible:
                newFloors = createFloors(floors, move, elevatorFloor, nextFloor)
                if len(newFloors[3]) == equipmentCount:
                    return moves + [move]
                elif isValid(floors, elevatorFloor, nextFloor):
                    queue.append((nextFloor, newFloors, moves + [moveId(move, elevatorFloor, nextFloor)]))
    
    return None

best = play(1, initial_floors)
print best
print len(best)

#printFloors(createFloors(floors, ['HyM', 'LiM'], 1, 2), 2)
#print possibleMoves(floors[0])