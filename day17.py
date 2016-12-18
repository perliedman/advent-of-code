#!/usr/bin/python

import sys
import heapq
import hashlib

passcode = sys.argv[1]

dirs = ['U', 'D', 'L', 'R']
ds = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def findPathTo(tx, ty):
    q = []
    initial = (1, 1, '')
    heapq.heappush(q, (0, initial))

    costs = {
        initial: 0
    }

    while q:
        (_, current) = heapq.heappop(q)
        (x, y, path) = current

        if x == tx and y == ty:
            return path

        md5 = hashlib.md5(passcode + path).hexdigest()
        open = [True if c >= 'a' else False for c in md5[0:4]]

        possibleMoves = [((x + dx, y + dy), d) for ((dx, dy), d, isOpen) in zip(ds, dirs, open) if x + dx > 0 and y + dy > 0 and x + dx < 5 and y + dy < 5 and isOpen]
        print x, y, passcode + path, path, md5, open, possibleMoves

        new_cost = costs[current] + 1
        for ((nx, ny), d) in possibleMoves:
            nextPath = path + d
            nextState = (nx, ny, nextPath)
            if nextState not in costs or new_cost < costs[nextState]:
                costs[nextState] = new_cost
                heapq.heappush(q, (abs(nx - tx) + abs(ny - ty), nextState))

print findPathTo(4, 4)
