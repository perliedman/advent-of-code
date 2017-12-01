#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

abbas = 0

for line in f.readlines():
	i = 1
	lc = line[0]
	inBracket = False
	isAbba = False
	for c in line[1:]:
		if c == '[':
			inBracket = True
		elif c == ']':
			inBracket = False
		elif c == lc and i > 1:
			first = line[i - 2]
			last = line[i + 1]
			if lc != first and first == last:
				if inBracket:
					isAbba = False
					break
				else:
					isAbba = True

		lc = c
		i += 1

	if isAbba:
		print line
		abbas += 1

print abbas
