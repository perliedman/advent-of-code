#!/usr/bin/python

import sys
import re

line_pattern = re.compile('([a-z\\-]+)-([0-9]+)\\[([a-z]+)\\]')

f = open(sys.argv[1], 'r')

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
		decoded = []
		for c in room:
			if c != '-':
				v = ord(c) - 97
				v = (v + sector) % (ord('z') - ord('a') + 1)
				decoded.append(chr(v + 97))
			else:
				decoded.append(' ')

		decoded = ''.join(decoded)

		if decoded.startswith('north'):
			print decoded, sector