#!/usr/bin/python

import sys
import re

def sortPair(a, b):
    c0 = cmp(a[0], b[0])
    return c0 if c0 else cmp(a[1], b[1])

f = open(sys.argv[1], 'r')

maxip = int(sys.argv[2])

lo = 0
hi = maxip

pattern = re.compile('(\\d+)\\-(\\d+)')

ranges = [tuple([int(x) for x in pattern.match(l).groups()[0:2]]) for l in f.readlines()]
ranges.sort(cmp=sortPair)

print ranges[0]

for (l, h) in ranges:
    if l <= lo and h >= lo:
        lo = h + 1

print lo, hi
