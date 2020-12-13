import sys
import math

with open(sys.argv[1], 'r') as f:
    instrs = [(l[0], int(l[1:])) for l in f.readlines()]

    # part 1
    d = 0
    x = y = 0

    for i, j in instrs:
        if i == 'N':
            y = y - j
        elif i == 'S':
            y = y + j
        elif i == 'E':
            x = x + j
        elif i == 'W':
            x = x - j
        elif i == 'L':
            d = d + j
        elif i == 'R':
            d = d - j
        elif i == 'F':
            r = d / 180 * math.pi
            x = x + math.cos(r) * j
            y = y - math.sin(r) * j
        else:
            raise Exception('Unknown move ' + i)

        #print(x,y,d)

    print(round(abs(x) + abs(y)))

    # Part 2
    def rotate(x, y, t):
        t = t / 180 * math.pi
        return (
            x * math.cos(t) + y * math.sin(t),
            -x * math.sin(t) + y * math.cos(t)
        )

    x = y = 0
    wp_x = 10
    wp_y = -1

    for i, j in instrs:
        if i == 'N':
            wp_y = wp_y - j
        elif i == 'S':
            wp_y = wp_y + j
        elif i == 'E':
            wp_x = wp_x + j
        elif i == 'W':
            wp_x = wp_x - j
        elif i == 'L':
            wp_x, wp_y = rotate(wp_x, wp_y, j)
        elif i == 'R':
            wp_x, wp_y = rotate(wp_x, wp_y, -j)
        elif i == 'F':
            x = x + j * wp_x
            y = y + j * wp_y
        else:
            raise Exception('Unknown move ' + i)

        print(i, j, 0, 0, wp_x, wp_y)

    print(round(abs(x) + abs(y)))
