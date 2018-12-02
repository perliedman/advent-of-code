from sys import stdin

def has(l, x):
    counts = {}
    for c in l:
        if c in counts:
            counts[c] = counts[c] + 1
        else:
            counts[c] = 1

    for (c, count) in counts.items():
        if count == x:
            return c

    return None

lines = [l.strip() for l in stdin.readlines()]

twos = [has(l, 2) for l in lines if has(l, 2)]
threes = [has(l, 3) for l in lines if has(l, 3)]

print twos
print threes
print len(twos)*len(threes)
