# This is not the way to do it...

from sys import stdin
import re

def intersection(r1, r2):
    (_, x11, y11, w1, h1) = r1
    (_, x21, y21, w2, h2) = r2
    (x12, y12) = (x11 + w1, y11 + h1)
    (x22, y22) = (x21 + w2, y21 + h2)

    if (x11 > x22 or x12 < x21 or
       y11 > y22 or y12 < y21):
        return 0

    xd = min(x12, x22) - max(x11, x21)
    yd = min(y12, y22) - max(y11, y21)

    print r1, r2, '=>', xd, yd

    return max(0, xd) * max(0, yd)

if __name__ == '__main__':
    line_pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    lines = [l.strip() for l in stdin.readlines()]
    rectangles = [[int(x) for x in line_pattern.match(l).groups()] for l in lines]

    sum = 0
    for i in xrange(0, len(rectangles)):
        for j in xrange(0, i):
            area = intersection(rectangles[i], rectangles[j])
            sum += area

    print sum
