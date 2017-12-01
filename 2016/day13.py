#!/usr/bin/python

import sys
import heapq

c = int(sys.argv[1])

def bitParity(x):
   x ^= x >> 16
   x ^= x >> 8
   x ^= x >> 4
   x &= 0xf

   return (0x6996 >> x) & 1;

def isWall(x, y):
    v = x * x + 3 * x + 2 * x * y + y + y * y + c
    return bitParity(v) == 1

def printWalls(s):
    for y in xrange(0, s):
        row = ['#' if isWall(x, y) else ' ' for x in xrange(0, s)]
        print ''.join(row)

def findPathTo(tx, ty):
    q = []
    initial = (1, 1)
    heapq.heappush(q, (0, initial))

    costs = {
        initial: 0
    }

    while q:
        (_, current) = heapq.heappop(q)
        (x, y) = current

        if x == tx and y == ty:
            break

        possibleMoves = [(x + dx, y + dy) for (dx, dy) in [(0, 1), (0, -1), (-1, 0), (1, 0)] if x + dx >= 0 and y + dy >= 0]
        possibleMoves = [(x, y) for (x, y) in possibleMoves if not isWall(x, y)]

        new_cost = costs[current] + 1
        for (nx, ny) in possibleMoves:
            if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                costs[(nx, ny)] = new_cost
                heapq.heappush(q, (abs(nx - tx) + abs(ny - ty), (nx, ny)))

    print costs[current]

findPathTo(int(sys.argv[2]), int(sys.argv[3]))
