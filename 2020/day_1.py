import sys

with open(sys.argv[1], 'r') as f:
    numbers = set([int(x) for x in f.readlines()])
    for x in numbers:
        y = 2020 - x
        if y in numbers:
            print(x, y, x * y)

    for x in numbers:
        y = 2020 - x
        for z in numbers:
            q = y - z
            if q in numbers:
                print(x, z, q, x + z + q, x * z * q)
