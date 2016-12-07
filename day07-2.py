#!/usr/bin/python

import sys

f = open(sys.argv[1], 'r')

def split_ip(s):
	hypernets = []
	supernets = []
	curr = []
	inHypernet = False

	for c in s:
		print c, curr
		if c == '[':
			inHypernet = True
			supernets.append(''.join(curr))
			curr = []
		elif c == ']':
			inHypernet = False
			hypernets.append(''.join(curr))
			curr = []
		else:
			curr.append(c)

	last = ''.join(curr)
	if len(last):
		supernets.append(last)

	return (supernets, hypernets)

def find_aba(s):
	print s
	abas = []
	i = 1
	for c in s[1:-1]:
		p = s[i - 1]
		n = s[i + 1]
		if c != p and p == n:
			abas.append(s[i - 1:i + 2])
		i += 1

	return abas

def find_bab(aba, s):
	f = aba[0]
	m = aba[1]
	bab = ''.join([m, f, m])

	return s.find(bab) >= 0

ssl = 0
for line in f.readlines():
	line = line[0:-1]
	(supernets, hypernets) = split_ip(line)

	is_ssl = False
	abas = reduce(lambda xs, x: xs + find_aba(x), supernets, [])
	print supernets, hypernets, abas
	for aba in abas:
		for hn in hypernets:
			if find_bab(aba, hn):
				is_ssl = True
				break

	if is_ssl:
		print line
		ssl +=1

print ssl
