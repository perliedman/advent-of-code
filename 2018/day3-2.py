from sys import stdin
import re


if __name__ == '__main__':
    line_pattern = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')

    lines = [l.strip() for l in stdin.readlines()]
    rectangles = [[int(x) for x in line_pattern.match(l).groups()] for l in lines]

    max_x = reduce(lambda a, (_, x, y, w, h): max(a, x + w), rectangles, 0)
    max_y = reduce(lambda a, (_, x, y, w, h): max(a, y + w), rectangles, 0)

    fabric = [[0 for x in range(max_x)] for x in range(max_y)]
    non_overlapped = set([id for (id, x, y, w, h) in rectangles])
    for (id, x, y, w, h) in rectangles:
        for i in xrange(x, x + w):
            for j in xrange(y, y + h):
                if fabric[j][i] != 0:
                    non_overlapped.discard(fabric[j][i])
                    non_overlapped.discard(id)
                fabric[j][i] = id

    print non_overlapped

