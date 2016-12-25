#!/usr/bin/python

import sys
import re
import itertools

f = open(sys.argv[1], 'r')

pattern = re.compile('([^\\s]+)\\s+(\\d+)T\\s+(\\d+)T\\s+(\\d+)T')

nodes = []
for l in f.readlines()[2:]:
    m = pattern.match(l)
    gs = m.groups()
    nodes.append((gs[0], int(gs[1]), int(gs[2]), int(gs[3])))

def isViable(a, b):
    return a[2] > 0 and a[0] != b[0] and a[2] < b[3]

def viablePairs(nodes):
    return [(a, b) for (a, b) in itertools.product(nodes, nodes) if isViable(a, b)]

def findPathFrom(sx, sy, nodes):
    q = []
    initial = (sx, sy, viablePairs(nodes))
    heapq.heappush(q, (0, initial))

    costs = {
        initial: 0
    }

    while q:
        (_, current) = heapq.heappop(q)
        (x, y, ps) = current

        if x == 0 and y == 0:
            break

        new_cost = costs[current] + 1
        for (a, b) in ps:
            if (nx, ny) not in costs or new_cost < costs[(nx, ny)]:
                costs[(nx, ny)] = new_cost
                heapq.heappush(q, (abs(nx - tx) + abs(ny - ty), (nx, ny)))

    print costs[current]


print len(viablePairs(nodes))
