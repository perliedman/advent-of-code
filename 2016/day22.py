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

pairs = [(a, b) for (a, b) in itertools.product(nodes, nodes) if isViable(a, b)]

print len(pairs)
