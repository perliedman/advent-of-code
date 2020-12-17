import sys
import re
from itertools import count
from functools import reduce

field_pattern = re.compile(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)')

def in_range(v, min, max):
    ir = v >= min and v <= max
    return ir

with open(sys.argv[1], 'r') as f:
    fields = []
    l = f.readline()
    while l.strip() != '':
        m = field_pattern.match(l)
        if m:
            g = m.groups()
            fields.append([g[0]] + [int(x) for x in g[1:]])
        l = f.readline()

    # your ticket
    f.readline()
    your_ticket = [int(x) for x in f.readline().split(',')]

    # nearby tickets
    f.readline()
    f.readline()
    l = f.readline()
    nearby_tickets = []
    while l.strip() != '':
        nearby_tickets.append([int(x) for x in l.split(',') if x])
        l = f.readline()

    def invalid_values(t):
        invalids = []
        for v in t:
            valid = False
            for f in fields:
                _, min1, max1, min2, max2 = f
                if in_range(v, min1, max1) or in_range(v, min2, max2):
                    valid = True
                    break
            if not valid:
                invalids.append((v, f))
        return invalids

    invalid = [invalid_values(t) for t in nearby_tickets]
    invalid_sums = [sum([v[0] for v in values]) for values in invalid]
    print(sum(invalid_sums))

    valid_tickets = [t for t in nearby_tickets if len(invalid_values(t)) == 0]
    candidates = []
    for i in range(len(valid_tickets[0])):
        values = [t[i] for t in valid_tickets]
        valid_fields = [n for n, min1, max1, min2, max2 in fields
            if all([in_range(x, min1, max1) or in_range(x, min2, max2) for x in values])]
        candidates.append(set(valid_fields))

    singles = set([list(x)[0] for x in candidates if len(x) == 1])
    while len(singles) < len(candidates):
        candidates = [c.difference(singles) if len(c) > 1 else c for c in candidates]
        singles = set([list(x)[0] for x in candidates if len(x) == 1])

    field_indexes = [(list(c)[0], i) for c, i in zip(candidates, count())]
    departure_indexes = [index for name, index in field_indexes if name.startswith('departure')]
    departure_values = [your_ticket[i] for i in departure_indexes]
    print(reduce(lambda a, x: a * x, departure_values))
