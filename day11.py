#!/usr/bin/python

import sys
import re
import time

f = open(sys.argv[1], 'r')

pos = {}
floors = []

equipment_pattern = re.compile('([a-z]+ generator|[a-z]+-compatible microchip)')

floorCount = 1
equipmentCount = 0
for line in f.readlines():
    equipment = equipment_pattern.findall(line)
    floor = set()
    floors.append(floor)
    for e in equipment:
        parts = e.split()
        if parts[1] == 'generator':
            eqId = parts[0][0:2].capitalize() + 'G'
        elif parts[1] == 'microchip':
            eqId = parts[0].split('-')[0][0:2].capitalize() + 'M'
        else:
            raise Exception('Unknown equipment type "' + parts[1] + '"')

        pos[eqId] = floorCount
        floor.add(eqId)
        equipmentCount += 1

    floorCount += 1

elevatorFloor = 1
moves = 0

def printFloors():
    global floors
    for i in xrange(4, 0, -1):
        f = floors[i - 1]
        print '* ' if i == elevatorFloor else '  ', i, ' '.join(f)

def findPair(f):
    for g in [g for g in f if g.endswith('G')]:
        m = g[0:2] + 'M'
        if m in f:
            return (g, m)
    return None

def move(eq, d):
    global floors, pos, elevatorFloor
    pFloor = floors[elevatorFloor - 1]
    nFloor = floors[elevatorFloor - 1 + d]

    print 'Moving ', eq, ' from floor', elevatorFloor, ' to floor ', elevatorFloor + d

    for eqId in eq:
        pFloor.remove(eqId)
        nFloor.add(eqId)
        pos[eqId] = elevatorFloor + d

    elevatorFloor += d

def generators(floor):
    return [g for g in floors[floor - 1] if g.endswith('G')]

def equipmentAbove(f):
    return [m for (m, floor) in pos.items() if floor > f]

def microchips(floor):
    return [m for m in floors[floor - 1] if m.endswith('M')]

def microchipsBelow(f):
    return [m for (m, floor) in pos.items() if m.endswith('M') and floor < f]

def assertValid():
    for i in range(1, 5):
        gens = generators(i)
        if len(gens):
            for c in microchips(i):
                if pos[c[0:2] + 'G'] != i:
                    raise Exception('%s on floor %d: %s' % (c, i - 1, ', '.join(floors[i - 1])))

print chr(0x9b)+chr(27)+'[2J'
print moves
printFloors()

#time.sleep(1)
while len(floors[3]) < equipmentCount and moves < 12:
#    print chr(0x9b)+chr(27)+'[2J'
    print moves

    if elevatorFloor < 1 or elevatorFloor > 4:
        raise Exception('Elevator floor out of range: ' + str(elevatorFloor))
    assertValid()

    floor = floors[elevatorFloor - 1]
    pair = findPair(floor)

    if pair and elevatorFloor < 4 and len(equipmentAbove(elevatorFloor)):
        floorGens = generators(elevatorFloor)
        chipsAtOrBelow = microchipsBelow(elevatorFloor)
        # If the pair is the only items on this floor, or there
        # are no microchips below this floor, move them up
        if len(floorGens) == 1 or len(chipsAtOrBelow) == 0:
            print "Rule 1"
            move(pair, 1)
        else:
            print "Rule 2"
            # There is at least one microchip on a lower floor,
            # use the microchip from the pair to go down to fetch it
            move([pair[1]], -1)
    else:
        chips = microchips(elevatorFloor)
        chipsWithLowerGen = [c for c in chips if pos[c[0:2] + 'G'] < elevatorFloor]

        # If one of the microchips on this floor has a generator on a lower floor,
        # take the chip to go down and bring the generator
        if len(chipsWithLowerGen):
            print "Rule 3"
            move(chipsWithLowerGen[0:1], -1)
        # Otherwise, if there are microchips on this floor, move as many of them as
        # possible up.
        elif len(chips) > 1 and elevatorFloor < 4:
            print "Rule 4"
            nextGens = generators(elevatorFloor + 1)
            move([c for c in chips[0:2] if len(nextGens) == 0 or pos[c[0:2] + 'G'] == elevatorFloor + 1], 1)
        # Otherwise, there's a microchip somewhere below, use one of the chips to
        # go bring it up
        else:
            print "Rule 5"
            move(chips[0:1], -1)

    printFloors()
    moves += 1

#    time.sleep(1)

print moves
