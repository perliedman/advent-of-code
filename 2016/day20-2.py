#!/usr/bin/python

import sys
import re

class Range:
    def __init__(self, lo, hi, next=None):
        self.lo = lo
        self.hi = hi
        self.next = next

    def intersects(self, r):
        return r.lo <= self.hi and r.hi >= self.lo

    def split(self, r):
        if r.lo > self.lo and r.hi < self.hi:
            rlo = Range(self.lo, r.lo - 1)
            rhi = Range(r.hi + 1, self.hi)
            return (rlo, rhi)
        elif r.hi < self.hi:
            return (Range(r.hi + 1, self.hi),)
        else:
            return (Range(self.lo, r.lo - 1),)

    def length(self):
        return self.hi - self.lo + 1

    def __str__(self):
        return '%d - %d (%d)' % (self.lo, self.hi, self.hi - self.lo + 1)

class RangeList:
    def __init__(self, lo, hi):
        self.head = Range(lo, hi)

    def removeRange(self, lo, hi):
        rr = Range(lo, hi)
        last = None
        curr = self.head
        while curr:
            if curr.intersects(rr):
                cnext = curr.next
                newRanges = curr.split(rr)
                print 'Split', curr, 'by', rr, 'into', [str(r) for r in newRanges]
                for nr in newRanges:
                    curr = nr
                    if last:
                        last.next = curr
                    else:
                        self.head = curr
                    last = curr
                curr.next = cnext

            last = curr
            curr = curr.next

    def count(self):
        r = self.head
        c = 0
        while r:
            c += r.length()
            r = r.next

        return c

    def __str__(self):
        r = []
        c = self.head
        while c:
            r.append(str(c))
            c = c.next

        return '\n'.join(r)

def sortPair(a, b):
    c0 = cmp(a[0], b[0])
    return c0 if c0 else cmp(a[1], b[1])

f = open(sys.argv[1], 'r')

maxip = int(sys.argv[2])

pattern = re.compile('(\\d+)\\-(\\d+)')

ranges = [tuple([int(x) for x in pattern.match(l).groups()[0:2]]) for l in f.readlines()]
ranges.sort(cmp=sortPair)

rangeList = RangeList(0, maxip)

for (l, h) in ranges:
    rangeList.removeRange(l, h)

print rangeList.count()