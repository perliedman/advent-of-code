#!/usr/bin/python

import sys
import re

def swapPositions(data, x, y):
    x = int(x)
    y = int(y)
    l = list(data)
    l[x], l[y] = l[y], l[x]
    return ''.join(l)

def swapLetters(data, x, y):
    # data = data.replace(x, '_')
    # print data
    # data = data.replace(y, x)
    # print data
    # data = data.replace('_', y)
    # print data
    # return data
    return data.replace(x, '_').replace(y, x).replace('_', y)

def rotateConstant(data, dir, x):
    x = int(x) % len(data)
    if dir == 'left':
        return data[x:] + data[:x]
    else:
        return data[-x:] + data[:-x]

def rotatePosition(data, x):
    i = data.index(x)
    if i >= 4:
        i += 1
    i = (i + 1) % len(data)

    return data[-i:] + data[:-i]

def reverse(data, x, y):
    x = int(x)
    y = int(y)
    s = data[x:y + 1]
    s = s[::-1]

    return data[:x] + s + data[y + 1:]

def movePosition(data, x, y):
    x = int(x)
    y = int(y)
    l = list(data)
    s = l[x]
    del l[x]
    l.insert(y, s)
    return ''.join(l)

commands = [
    (re.compile('swap position (\\d+) with position (\\d+)'), swapPositions),
    (re.compile('swap letter (\\w) with letter (\\w)'), swapLetters),
    (re.compile('rotate (left|right) (\\d+) steps*'), rotateConstant),
    (re.compile('rotate based on position of letter (\\w)'), rotatePosition),
    (re.compile('reverse positions (\\d+) through (\\d+)'), reverse),
    (re.compile('move position (\\d+) to position (\\d+)'), movePosition),
]

f = open(sys.argv[1], 'r')
data = sys.argv[2]

i = 1
for l in f.readlines():
    handled = False
    for (pattern, handler) in commands:
        m = pattern.match(l)
        if m:
            data = handler(data, *m.groups())
            print '%3d %s' % (i, data)
            handled = True
            i += 1
            break;

    if not handled:
        raise Exception('Unhandled line: ' + l)

# print rotatePosition(sys.argv[1], sys.argv[2])
