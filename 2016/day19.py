#!/usr/bin/python

import sys

n = int(sys.argv[1])

r = 1
f = 1

while n > 1:
	if n % 2 == 1:
		f += (1 << r)

	r += 1
	n = n / 2

print f
