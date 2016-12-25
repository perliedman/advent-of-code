#!/usr/bin/python

import sys
import re

p = re.compile('[^ ]*([a-z0-9])\\1\\1[^ ]* [^$]*([a-z0-9])\\2\\2\\2\\2[^ ]*$')

for l in open(sys.argv[1], 'r').readlines():
    if not p.match(l):
        print l
