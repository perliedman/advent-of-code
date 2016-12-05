#!/usr/bin/python

import sys

x = 0
y = 0
a = 0
dy = [-1, 0, 1, 0]
dx = [0, -1, 0, 1]

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

	x += dx[a] * number
	y += dy[a] * number

	#print dir, number, a, x, y, dx, dy

print abs(x) + abs(y)
