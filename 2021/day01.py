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
    prev_sum = None
    sum = 0
    prevs = []
    n_incs = 0
    for i in range(len(depths)):
        prevs.append(depths[i])
        sum += depths[i]
        if len(prevs) == 4:
            sum -= prevs[0]
            prevs = prevs[1:]

#            print(prev_sum, sum)
            if prev_sum and sum > prev_sum:
                n_incs = n_incs + 1

        if len(prevs) == 3:
            prev_sum = sum

    print(n_incs)

with open(sys.argv[1], 'r') as f:
    depths = [int(x) for x in f.readlines()]

part1(depths)
part2(depths)
