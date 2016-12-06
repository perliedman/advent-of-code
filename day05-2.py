#!/usr/bin/python

import sys
from hashlib import md5

k = sys.argv[1]
i = 0
c = 0
passw = [' '] * 8

while c < 8:
	hash = md5(k + str(i)).hexdigest()
	if hash.startswith('00000'):
		p = hash[5]
		if p >= '0' and p <= '7':
			p = int(p)
			if passw[p] == ' ':
				passw[int(p)] = hash[6]
				print i, hash, p, ''.join(passw)
				if len(filter(lambda x: x != ' ', passw)) == 8:
					break

	i += 1

print ''.join(passw)
