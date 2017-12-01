#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

possible = 0

for line in f.readlines():
	sides = map(int, line.split())

	if sides[0] + sides[1] > sides[2] and \
	   sides[1] + sides[2] > sides[0] and \
	   sides[2] + sides[0] > sides[1]:
	   possible += 1

print possible
