#!/usr/bin/python

import sys
from hashlib import md5

k = sys.argv[1]
i = 0
c = 0
passw = []

while c < 8:
	hash = md5(k + str(i)).hexdigest()
	if hash.startswith('00000'):
		passw.append(hash[5])
		print ''.join(passw)
		c += 1

	i += 1
	if i % 10000 == 0:
		print i

print ''.join(passw)
