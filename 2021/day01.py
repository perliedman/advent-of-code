import sys

def part1(depths):
    prev = depths[0]
    n_incs = 0
    for i in range(1, len(depths)):
        if depths[i] > prev:
            n_incs = n_incs + 1

        prev = depths[i]

    print(n_incs)


def part2(depths):
    incs = [i for i in range(len(depths) - 3) if sum(depths[i + 1:i + 4]) > sum(depths[i:i + 3])]
    print(len(incs))

with open(sys.argv[1], 'r') as f:
    depths = [int(x) for x in f.readlines()]

part1(depths)
part2(depths)
