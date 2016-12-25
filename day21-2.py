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
    return data.replace(x, '_').replace(y, x).replace('_', y)

def rotateConstant(data, dir, x):
    x = int(x) % len(data)
    if dir == 'right':
        return data[x:] + data[:x]
    else:
        return data[-x:] + data[:-x]


# 0 -> 1
# 1 -> 3
# 2 -> 5
# 3 -> 7
# --
# 4 -> 10
# 6 -> 14 => 14 % 8 = 6
#
# p = p0 + p0 + 1 = 2 * p0 + 1 if p0 < 4 => p <= 7    => p0 = (p - 1) / 2
# p = p0 + p0 + 2 = 2 * p0 + 2 if p0 >= 4 => p >= 10  => p0 = (p - 2) / 2
# p0 = (p - 1) / 2
def rotatePosition(data, x):
    """
    >>> rotatePosition('aebcdhfg', 'f')
    'aebcdhfg'
    >>> rotatePosition('ecabd', 'b')
    'abdec'
    >>> rotatePosition('decab', 'd')
    'ecabd'
    """
    p = data.index(x)

    if p % 2:
        p0 = (p - 1) / 2
    else:
        p0 = (p - 2) / 2

    while p0 < 0:
        p0 += len(data)

    i = p0 % len(data)
    if i >= 4:
        i += 1

    i = (i + 1) % len(data)

    return data[i:] + data[:i]

def reverse(data, x, y):
    x = int(x)
    y = int(y)
    s = data[x:y + 1]
    s = s[::-1]

    return data[:x] + s + data[y + 1:]

def movePosition(data, y, x):
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

if __name__ == '__main__':
    if sys.argv[1] == 'test':
        import doctest
        doctest.testmod()

        sys.exit(0)

f = open(sys.argv[1], 'r')
data = sys.argv[2]

lines = f.readlines()
lines.reverse()
i = 1
for l in lines:
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

print data
