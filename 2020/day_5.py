import sys

def seat_to_binary(x):
    return x \
        .replace('F', '0') \
        .replace('B', '1') \
        .replace('R', '1') \
        .replace('L', '0')

with open(sys.argv[1], 'r') as f:
    seat_ids = [int(seat_to_binary(x), 2) for x in f.readlines()]
    seat_ids.sort()
    print(seat_ids[-1])

    for i in range(1, len(seat_ids)):
        if seat_ids[i - 1] != seat_ids[i] - 1:
            print(seat_ids[i] - 1)
