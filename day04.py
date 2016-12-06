#!/usr/bin/python

import sys
import re

line_pattern = re.compile('([a-z\\-]+)-([0-9]+)\\[([a-z]+)\\]')

f = open(sys.argv[1], 'r')

sector_sum = 0


for line in f.readlines():
	match = line_pattern.match(line)

	room = match.group(1)
	sector = int(match.group(2))
	cs = match.group(3)

	chars = {}
	for part in room.split('-'):
		for c in part:
			if c in chars:
				chars[c] += 1
			else:
				chars[c] = 1

	chars = chars.items()
	chars.sort(cmp=lambda a, b: cmp(b[1], a[1]) or cmp(a[0], b[0]))
	chars = ''.join(map(lambda x: x[0], chars))

	if chars[0:5] == cs:
		sector_sum += sector

print sector_sum
