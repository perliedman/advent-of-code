#!/usr/bin/python

import sys
import re

file = open(sys.argv[1], 'r')

d = file.read()
d = re.sub('\\s', '', d)

c = 0

r = []

while c < len(d):
    if d[c] == '(':
        c += 1
        header = []
        while d[c] != ')':
            header.append(d[c])
            c += 1

        header = ''.join(header)
        match = re.match('([0-9]+)x([0-9]+)', header)
        length = int(match.group(1))
        times = int(match.group(2))

        repeat = d[c + 1:c + length + 1]
        for _ in xrange(0, times):
            r.append(repeat)

        c += length + 1
    else:
        r.append(d[c])
        c += 1

r = ''.join(r)

print len(r)
