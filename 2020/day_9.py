import sys

with open(sys.argv[1], 'r') as f:
    numbers = [int(x) for x in f.readlines()]

    preamble = 25
    xs = numbers[0:preamble]

    def valid(y):
        seen = set()
        for a in xs:
            if (y - a) in seen:
                return True
            seen.add(a)
        return False

    for y in numbers[preamble:]:
        if not valid(y):
            non_valid = y
            break

        xs = xs[1:]
        xs.append(y)

    print(non_valid)

    def is_weakness(candidates):
        for i in range(0, len(candidates) - 1):
            t = candidates[i:]
            s = sum(t)
            if s == non_valid:
                return t
        return None

    candidates = []
    weakness = None
    for y in numbers:
        candidates.append(y)
        
        s = sum(candidates)
        while s > non_valid:
            cset = is_weakness(candidates)
            if cset:
                weakness = min(cset) + max(cset)
                break
            candidates = candidates[1:]
            s = sum(candidates)

    if weakness:
        print(weakness)
    else:
        print('None found')
