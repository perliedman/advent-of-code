from difflib import SequenceMatcher
from sys import stdin

lines = [l.strip() for l in stdin.readlines()]

for i in xrange(0, len(lines)):
    for j in xrange(0, i):
        m = SequenceMatcher(None, lines[i], lines[j])
        matches = m.get_matching_blocks()
        if sum([m[2] for m in matches]) == len(lines[i]) - 1:
            print lines[i], lines[j], ' => ', ''.join([lines[i][m[0]:m[0] + m[2]] for m in matches])
