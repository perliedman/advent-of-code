#!/usr/bin/python

import sys
import itertools

f = open(sys.argv[1], 'r')

possible = 0

alllines = f.readlines()
done = False

def column(rows, c):
	return map(lambda row: row[c], rows)

def is_possible(sides):
	return sides[0] + sides[1] > sides[2] and \
	   sides[1] + sides[2] > sides[0] and \
	   sides[2] + sides[0] > sides[1]

while not done:
	lines = alllines[:3]
	alllines = alllines[3:]
	done = len(lines) != 3

	if not done:
		sides = map(lambda line: map(int, line.split()), lines)
		possible += len(filter(lambda x: x, map(lambda c: is_possible(column(sides, c)), range(0, 3))))

print possible
