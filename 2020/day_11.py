import sys

dirs = [
    [-1, 0],
    [-1, 1],
    [0, 1],
    [1, 1],
    [1, 0],
    [1, -1],
    [0, -1],
    [-1, -1]
]

def count(l, c):
    count = 0;
    for y in range(len(layout)):
        for x in range(len(layout[y])):
            if l[y][x] == c:
                count = count + 1

    return count

with open(sys.argv[1], 'r') as f:
    layout = [list(l.strip()) for l in f.readlines()]

    def step_1(l):
        changed = False
        next = [x[:] for x in l]
        for y in range(len(l)):
            for x in range(len(l[y])):
                neighbours = [l[y + yd][x + xd] for yd, xd in dirs if x + xd >= 0 and x + xd < len(l[y]) and y + yd >= 0 and y + yd < len(l)]
                if l[y][x] == 'L' and len([x for x in neighbours if x == '#']) == 0:
                    next[y][x] = '#'
                    changed = True
                elif l[y][x] == '#' and len([x for x in neighbours if x == '#']) >= 4:
                    next[y][x] = 'L'
                    changed = True

        return (next, changed)

    def step_2(l):
        def is_occupied(x, y, xd, yd):
            x = x + xd
            y = y + yd
            while x >= 0 and y >= 0 and x < len(l[0]) and y < len(l):
                if l[y][x] == '#':
                    return True
                elif l[y][x] == 'L':
                    return False
                x = x + xd
                y = y + yd

            return False

        changed = False
        next = [x[:] for x in l]
        for y in range(len(l)):
            for x in range(len(l[y])):
#                neighbours = [l[y + yd][x + xd] for yd, xd in dirs if x + xd >= 0 and x + xd < len(l[y]) and y + yd >= 0 and y + yd < len(l)]
                n_occupied = len([True for xd, yd in dirs if is_occupied(x, y, xd, yd)])
                if l[y][x] == 'L' and n_occupied == 0:
                    next[y][x] = '#'
                    changed = True
                elif l[y][x] == '#' and n_occupied >= 5:
                    next[y][x] = 'L'
                    changed = True

        return (next, changed)

    has_changed = True
    layout_1 = layout
    while has_changed:
        (layout_1, has_changed) = step_1(layout_1)
        # print(layout, has_changed)

    print(count(layout_1, '#'))

    has_changed = True
    layout_2 = layout
    while has_changed:
        (layout_2, has_changed) = step_2(layout_2)
        print('\n'.join([''.join(l) for l in layout_2]), has_changed)
        print()

    print(count(layout_2, '#'))
