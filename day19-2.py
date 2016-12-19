#!/usr/bin/python

import sys

n = int(sys.argv[1])

r = 1
lo = 1
hi = n
s = 1

while n > 1:
	if n == 2:
		hi = lo
	elif n % 3 == 0:
		lo += s * 2
		s = s * 2 + 1
	elif n % 2 == 1:
		lo += s
		hi -= s
		s *= 2
	else:
		hi -= s * 2

#	if (hi - lo) / s + 1 != n:
#		raise Exception('Doh %d %d %d %d' % (lo, hi, (hi - lo) / s + 1, n))
	n = (hi - lo) / s + 1
	print lo, hi, s, n

print lo, hi
