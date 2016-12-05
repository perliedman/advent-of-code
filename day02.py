#!/usr/bin/python

import sys

keys = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
]

f = open(sys.argv[1], 'r')

for line in f.readlines():
	x = 1
	y = 1

	for c in line:
		if c == 'U':
			y -= 1
		elif c == 'D':
			y += 1
		elif c == 'L':
			x -= 1
		elif c == 'R':
			x += 1

		x = max(0, min(2, x))
		y = max(0, min(2, y))

	print keys[y][x]

