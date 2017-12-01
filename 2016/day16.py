#!/usr/bin/python

import sys

def dragon(a):
    """
    >>> dragon('0')
    '001'
    >>> dragon('1')
    '100'
    >>> dragon('11111')
    '11111000000'
    >>> dragon('111100001010')
    '1111000010100101011110000'
    """
    b = ''.join(['0' if c == '1' else '1' for c in a[::-1]])
    
    return a + '0' + b


def checksum(d):
    """
    >>> checksum('110010110100')
    '100'
    """
    while True:
        pairs = [d[i:i + 2] for i in xrange(0, len(d), 2)]
        cs = ''.join(['1' if p[0] == p[1] else '0' for p in pairs])
        if len(cs) % 2 == 0:
            d = cs
        else:
            return cs


def fill(state, l):
    """
    >>> fill('10000', 20)
    '01100'
    """
    while len(state) < l:
        state = dragon(state)

    return checksum(state[0:l])

if sys.argv[1] == 'test':
    import doctest
    doctest.testmod()
    print 'Done'
else:
    print fill(sys.argv[1], int(sys.argv[2]))
