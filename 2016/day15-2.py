#!/usr/bin/python

import sys
import re

line_pattern = re.compile('Disc #([0-9]+) has ([0-9]+) positions; at time=([0-9]+), it is at position ([0-9]+).')

pos = []
for l in open(sys.argv[1], 'r').readlines():
    gs = line_pattern.match(l).groups()
    print gs
    pos.append((int(gs[3]), int(gs[1])))

pos.append((0, 11))

def correct(pos, t):
    y = 1
    for (p, ps) in pos:
        if (p + y + t) % ps != 0:
            return False
        y += 1
    return True

t = 0
while not correct(pos, t):
    t += 1


y = 1
for (p, ps) in pos:
    print p, y, t, ps, (p + y + t) % ps
    y += 1
print t
