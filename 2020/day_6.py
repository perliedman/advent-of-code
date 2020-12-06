import sys

with open(sys.argv[1], 'r') as f:
    groups = []
    current_group = None
    for l in f.readlines():
        l = l.strip()
        if len(l) > 0:
            # use union for part 1
            current_group = current_group.intersection(set(l)) if current_group != None else set(l)
        else:
            groups.append(current_group)
            current_group = None

    if current_group:
        groups.append(current_group)

print(sum([len(g) for g in groups]))
