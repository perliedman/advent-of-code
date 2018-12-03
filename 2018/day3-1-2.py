from sys import stdin
import re


if __name__ == '__main__':
    line_pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    lines = [l.strip() for l in stdin.readlines()]
    rectangles = [[int(x) for x in line_pattern.match(l).groups()] for l in lines]

    max_x = reduce(lambda a, (_, x, y, w, h): max(a, x + w), rectangles, 0)
    max_y = reduce(lambda a, (_, x, y, w, h): max(a, y + w), rectangles, 0)

    fabric = [[0 for x in range(max_x)] for x in range(max_y)]

    overlap = 0
    for (id, x, y, w, h) in rectangles:
        print id, x, y, w, h
        for i in xrange(x, x + w):
            for j in xrange(y, y + h):
                if fabric[j][i] == 1:
                    overlap += 1
                fabric[j][i] += 1

    for j in xrange(0, max_y):
        print ''.join(str(fabric[j][i]) for i in xrange(0, max_x))

    print overlap

