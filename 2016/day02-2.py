#!/usr/bin/python

import sys

_ = None
A = 'A'
B = 'B'
C = 'C'
D = 'D'

keys = [
    [_, _, 1, _, _],
    [_, 2, 3, 4, _],
    [5, 6, 7, 8, 9],
    [_, A, B, C, _],
    [_, _, D, _, _],
    ]

f = open(sys.argv[1], 'r')

for line in f.readlines():
	x = 0
	y = 2

	for c in line:
		px = x
		py = y

		if c == 'U':
			y -= 1
		elif c == 'D':
			y += 1
		elif c == 'L':
			x -= 1
		elif c == 'R':
			x += 1

		x = max(0, min(4, x))
		y = max(0, min(4, y))

		if keys[y][x] is None:
			x = px
			y = py

	print keys[y][x]

