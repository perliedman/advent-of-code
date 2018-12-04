from sys import stdin
from collections import defaultdict
from itertools import count
import re

lines = [l.strip() for l in stdin.readlines()]
line_pattern = re.compile(r'\[([\d\-: ]+)\] (.*)')
shift_start_pattern = re.compile(r'Guard #(\d+) begins shift')

periods = [line_pattern.match(l).groups() for l in lines]
periods.sort(lambda x,y: cmp(x[0], y[0]))

guards = defaultdict(lambda: [0] * 60)

def parse_minute(t):
    return int(re.match('\d+-\d+-\d+ \d+:(\d+)', t).group(1))

minute = 0
asleep = False
t = None
for p in periods:
    shift_match = shift_start_pattern.match(p[1])
    if shift_match:
        if asleep:
            for i in range(minute, 60):
                t[i] += 1

        current_guard = shift_match.group(1)
        t = guards[current_guard]
        minute = 0
        asleep = False
    else:
        to_m = parse_minute(p[0])
        if asleep:
            for i in range(minute, to_m):
                t[i] += 1

        minute = to_m
        asleep = p[1] == 'falls asleep'

if asleep:
    for i in range(minute, 60):
        t[i] += 1

guard_totals = [(k, sum(v)) for (k, v) in guards.items()]
guard_totals.sort(lambda a, b: cmp(b[1], a[1]))

def get_most_sleepy_minute(id):
    return reduce(lambda (m, h), (i, x): (m, h) if x < h else (i, x), zip(count(), guards[id]))

sleepy_guard_id = guard_totals[0][0]
(most_sleepy_minute, how_sleepy) = get_most_sleepy_minute(sleepy_guard_id)

# print '\n'.join(['#%s: %s' % (k, str(v)) for (k, v) in guards.items()])
# print guard_totals
print sleepy_guard_id, most_sleepy_minute
print '#1', int(sleepy_guard_id) * most_sleepy_minute

guard_max = [(id, get_most_sleepy_minute(id)) for id in guards.keys()]
guard_max.sort(lambda (id1, (m1, h1)), (id2, (m2, h2)): cmp(h2, h1))

(id, (m, h)) = guard_max[0]
print id, m, h
print '#2', int(id) * m
