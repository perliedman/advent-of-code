#!/usr/bin/python

import sys
import heapq
import hashlib

passcode = sys.argv[1]

dirs = ['U', 'D', 'L', 'R']
ds = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def printPath(p):
    x = 1
    y = 1

    print '-----------'
    print 'Printing path of length', len(p)
    step = 0
    for d in p:
        i = dirs.index(d)
        md5 = hashlib.md5(passcode + p[0:step]).hexdigest()
        open = [True if c > 'a' else False for c in md5[0:4]]

        print d, (x, y), md5[0:4], open

        if not open[i]:
            raise Exception('*** INVALID MOVE ***')

        x += ds[i][0]
        y += ds[i][1]
        if x < 1 or y < 1 or x > 4 or y > 4:
            print d, 'Outside bounds:', (x, y)
        elif x == 4 and y == 4:
            print d, 'At target'

        step += 1

def findPathTo(tx, ty):
    q = []
    initial = (1, 1, '')
    heapq.heappush(q, (0, initial))

    costs = {
        initial: 0
    }

    evaluated = 0
    complete = 0
    best = None

    while q:
        evaluated += 1

        (_, current) = heapq.heappop(q)
        (x, y, path) = current

        if evaluated % 10000 == 0:
            print len(path), (len(q)), best

        if x == tx and y == ty:
            if not best or len(path) > best:
                best = len(path)
                complete += 1
                printPath(path)

#                if complete == 10:
#                    return best
        else:
            md5 = hashlib.md5(passcode + path).hexdigest()
            open = [True if c > 'a' else False for c in md5[0:4]]

            possibleMoves = [((x + dx, y + dy), d) for ((dx, dy), d, isOpen) in zip(ds, dirs, open)
                             if x + dx > 0 and y + dy > 0 and x + dx < 5 and y + dy < 5 and isOpen]

            new_cost = costs[current] + 1
            for ((nx, ny), d) in possibleMoves:
                nextPath = path + d
                nextState = (nx, ny, nextPath)
                if nextState not in costs or new_cost < costs[nextState]:
                    costs[nextState] = new_cost
                    heapq.heappush(q, (-len(nextPath), nextState))

    return best

print findPathTo(4, 4)
