#!/usr/bin/python

import sys

x = 0
y = 0
a = 0
dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]

grid = {}

for d in sys.argv[1:]:
	dir = d[0].lower()

	if d.endswith(','):
		number = int(d[1:-1])
	else:
		number = int(d[1:])

	if dir == 'l':
		a = (a + 1) % len(dy)
	else:
		a = a - 1
		if a < 0:
			a += len(dy)

	for _ in xrange(0, number):
		if x in grid:
			row = grid[x]
		else:
			row = grid[x] = {}

		if y in row:
			print abs(x) + abs(y), x, y
		else:
			row[y] = True

		x += dx[a]
		y += dy[a]

	#print dir, number, a, x, y, dx, dy
