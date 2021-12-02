# -*- coding: UTF-8
import sys

def part1(commands):
    pos = [0, 0]
    for (dir, step) in commands:
        if dir == 'forward':
            pos[0] += step
        elif dir == 'down':
            pos[1] += step
        elif dir == 'up':
            pos[1] -= step
        else:
            raise Exception('Uäuäuä')

    print(pos[0] * pos[1])

def part2(commands):
    pos = [0, 0, 0]
    for (dir, step) in commands:
        if dir == 'forward':
            pos[0] += step
            pos[1] += pos[2] * step
        elif dir == 'down':
            pos[2] += step
        elif dir == 'up':
            pos[2] -= step
        else:
            raise Exception('Uäuäuä')

    print(pos[0] * pos[1])

with open(sys.argv[1], 'r') as f:
    commands = [(dir, int(step)) for (dir, step) in [l.split(' ') for l in f.readlines()]]
    part1(commands)
    part2(commands)
