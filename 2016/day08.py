#!/usr/bin/python

import sys
import re

f = open(sys.argv[1], 'r')

COLS = 50
ROWS = 6

screen = [False]*(COLS*ROWS)

def rotate(s, x):
    return s[-x:] + s[0:-x]

for line in f.readlines():
    parts = line.split()

    if parts[0] == 'rect':
        dim = re.match('([0-9]+)x([0-9]+)', parts[1])
        w = int(dim.group(1))
        h = int(dim.group(2))
        i = 0
        for y in xrange(0, h):
            for x in xrange(0, w):
                screen[i] = True
                i += 1
            i += COLS - w
    elif parts[0] == 'rotate':
        p = int(re.match('.=([0-9]+)', parts[2]).group(1))
        a = int(parts[4])

        if parts[1] == 'column':
            i = p
            col = []
            for _ in xrange(0, ROWS):
                col.append(screen[i])
                i += COLS
            col = rotate(col, a)
            i = p
            for r in xrange(0, ROWS):
                screen[i] = col[r]
                i += COLS
        elif parts[1] == 'row':
            i = COLS * p
            row = screen[i:i + COLS]

            screen[i:i + COLS] = rotate(row, a)
        else:
            raise Exception('Unknown rotate %s' % (parts[1]))
    else:
        raise Exception('Unknown command %s' % (parts[0]))

i = 0
for y in xrange(0, ROWS):
    row = []
    for x in xrange(0, COLS):
        row.append('#' if screen[i] else '.')
        i += 1

    print ''.join(row)

print len([x for x in screen if x])
