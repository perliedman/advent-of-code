# -*- coding: UTF-8
import sys
import re

def line(world, x1, y1, x2, y2, ignore_diags):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 or dy == 0:
        (x1, x2) = (x1, x2) if x1 < x2 else (x2, x1)
        (y1, y2) = (y1, y2) if y1 < y2 else (y2, y1)
        if dx == 0:
            for y in range(y1, y2 + 1):
                world[y][x1] += 1
        elif dy == 0:
            for x in range(x1, x2 + 1):
                world[y1][x] += 1
    elif not ignore_diags:
        if abs(dx) != abs(dy):
            raise Exception('Not a diagonal.')

        sx = 1 if dx > 0 else - 1
        sy = 1 if dy > 0 else - 1
        for i in range(abs(dx) + 1):
            world[y1 + sy * i][x1 + i * sx] += 1


def create_world(lines):
    max_x = max([c[0] for c in lines] + [c[2] for c in lines]) + 1
    max_y = max([c[1] for c in lines] + [c[3] for c in lines]) + 1

    world = [[0 for x in range(max_x)] for y in range(max_y)]
    return world


def world_to_str(world):
    return '\n'.join([''.join([str(col) if col else '.' for col in row]) for row in world])


def part1(lines):
    world = create_world(lines)
    for l in lines:
        line(world, *l, True)

    s = sum([1 for row in world for cell in row if cell >= 2])
    print(s)


def part2(lines):
    world = create_world(lines)
    for l in lines:
        line(world, *l, False)

    print(world_to_str(world))
    s = sum([1 for row in world for cell in row if cell >= 2])
    print(s)


if __name__ == '__main__':
    line_pattern = re.compile(r'(\d+),(\d+) -> (\d+),(\d+)')
    with open(sys.argv[1], 'r') as f:
        lines = [[int(c) for c in line_pattern.match(l).groups()] for l in f.readlines()]
        part1(lines)
        part2(lines)
