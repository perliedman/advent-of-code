#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

c = f.readlines()
i = 0
regs = {
    'a': 0,
    'b': 0,
    'c': 1,
    'd': 0
}

def val(v):
    if v in regs:
        return regs[v]
    else:
        return int(v)

while i < len(c):
    parts = c[i].split()
    if parts[0] == 'cpy':
        regs[parts[2]] = val(parts[1])
    elif parts[0] == 'inc':
        regs[parts[1]] += 1
    elif parts[0] == 'dec':
        regs[parts[1]] -= 1
    elif parts[0] == 'jnz':
        if val(parts[1]) != 0:
            i += int(parts[2])
            continue
    else:
        raise Exception('Unknown instruction ' + c[i])

#    print i, ' ', c[i], ' ', regs

    i += 1

print regs
