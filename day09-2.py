#!/usr/bin/python

import sys
import re

file = open(sys.argv[1], 'r')

d = file.read()
d = re.sub('\\s', '', d)

c = 0

def decompress(length, indent=''):
    global c, d

    r = 0
    end = c + length
    while c < end:
        if d[c] == '(':
            c += 1
            header = []
            while d[c] != ')':
                header.append(d[c])
                c += 1
            header = ''.join(header)
            match = re.match('([0-9]+)x([0-9]+)', header)
            header = ''.join(header)
            length = int(match.group(1))
            times = int(match.group(2))
            c += 1
            r += decompress(length, indent + '  ') * times
        else:
            r += 1
            c += 1

    return r

r = decompress(len(d))

print r
