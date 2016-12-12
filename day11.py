#!/usr/bin/python

import sys
import re
import time
import itertools

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

def isValid(floors):
    for i in range(1, 5):
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
    return ''.join(move) + ';' + f + ';' + t

def play(elevatorFloor, floors, moves, best):
    floorI = elevatorFloor - 1
    candFloors = [f for f in [elevatorFloor + 1, elevatorFloor - 1] if f > 0 and f < 5]
    minMoves = 1e9
    for nextFloor in candFloors:
        for move in [m for m in possibleMoves(floors[floorI]) if not moveId(m, elevatorFloor, nextFloor) in moves]:
            oldCurr = floors[floorI][:]
            oldNext = floors[nextFloor - 1][:]
            floors[floorI] = [eqId for eqId in floors[floorI] if not eqId in move]
            floors[nextFloor - 1] += move

            if len(floors[3]) == equipmentCount:
                floors[floorI] = oldCurr
                floors[nextFloor - 1] = oldNext
                #print moves
                return moves + [moveId(move, elevatorFloor, nextFloor)]
            elif isValid(floors):
                if moves < best - 2:
                    candidateMoves = play(nextFloor, floors, moves + [moveId(move, elevatorFloor, nextFloor)], best)
                    if len(candidateMoves) < len(minMoves):
                        minMoves = candidateMoves
                        best = min(len(minMoves), best)
#                else:
#                    print 'Pruned at ', moves

            floors[floorI] = oldCurr
            floors[nextFloor - 1] = oldNext

    return minMoves

print play(1, initial_floors, [], 200)

#printFloors(createFloors(floors, ['HyM', 'LiM'], 1, 2), 2)
#print possibleMoves(floors[0])