#!/usr/bin/python

import sys
import re
import itertools
import heapq

namePattern = re.compile('x(\\d+)-y(\\d)+')
def nameToCoords(n):
    m = namePattern.search(n)
    return tuple([int(c) for c in m.groups()])

f = open(sys.argv[1], 'r')

pattern = re.compile('([^\\s]+)\\s+(\\d+)T\\s+(\\d+)T\\s+(\\d+)T')

nodes = []
for l in f.readlines()[2:]:
    m = pattern.match(l)
    gs = m.groups()
    nodes.append((nameToCoords(gs[0]), int(gs[1]), int(gs[2]), int(gs[3])))

def isViable(a, b):
    return a[2] > 0 and a[0] != b[0] and a[2] < b[3]

def viablePairs(nodes):
    return [(a, b) for (a, b) in itertools.product(nodes, nodes) if isViable(a, b)]

def findPathFrom(nodes):
    q = []

    viable = [(a[0], b[0]) for (a, b) in viablePairs(nodes)]
    empty = next(n for n in nodes if n[2] == 0)[0]
    target = reduce(lambda t, n: t if t[0][0] > n[0][0] or t[0][1] < n[0][1] else n, nodes)[0]
    maxx = reduce(lambda m, n: max(m, n[0][0]), nodes, 0)
    maxy = reduce(lambda m, n: max(m, n[0][1]), nodes, 0)
    stops = set([n[0] for n in nodes if n[1] > 100])
    dirs = [(1,0), (-1, 0), (0, -1), (0, 1)]

    print stops

    initial = (empty, target)
    heapq.heappush(q, (0, initial))

    costs = {
        initial: 0
    }

    while q:
        (_, current) = heapq.heappop(q)
        (empty, target) = current

        if target[0] == 0 and target[1] == 0:
            return costs[current]

        new_cost = costs[current] + 1

        (ex, ey) = empty
        possible = [(ex + dx, ey + dy) for (dx, dy) in dirs if 
            ex + dx >= 0 and ex + dx <= maxx and
            ey + dy >= 0 and ey + dy <= maxy]
        possible = [(nx, ny) for (nx, ny) in possible if (nx, ny) not in stops]

        print new_cost, empty, target, possible
        for (nx, ny) in possible:
            if nx == target[0] and ny == target[1]:
                newTarget = empty
            else:
                newTarget = target

            newState = ((nx, ny), newTarget)

            if newState not in costs or new_cost < costs[newState]:
                costs[newState] = new_cost
                nearbyStops = [True for (dx, dy) in dirs if (nx + dx, ny + dy) in stops]
                # score = nx / 2 + ny / 2 + abs(nx - newTarget[0]) + abs(ny - newTarget[1]) + len(nearbyStops) * 10
                score = 0
                heapq.heappush(q, (score, newState))

    return None


print findPathFrom(nodes)
