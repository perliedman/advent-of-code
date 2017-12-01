#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

lines = f.readlines()
cols = map(lambda _: {}, xrange(0, len(lines[0])))

for line in lines:
	i = 0
	for c in line:
		if c in cols[i]:
			cols[i][c] += 1
		else:
			cols[i][c] = 1

		i += 1

cols = map(lambda c: c.items(), cols)

for col in cols:
	col.sort(cmp=lambda a, b: cmp(b[1], a[1]))

print ''.join(map(lambda c: c[0][0], cols))
