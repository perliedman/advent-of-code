import sys
import re

pattern = re.compile(r'^(\d+)-(\d+)\s+(\w):\s+(.*)$')

def valid_1(((minimum, maximum, c, password))):
    count = 0
    for pc in password:
        if pc == c:
            count = count + 1

    return count >= int(minimum) and count <= int(maximum)

def valid_2(((i, j, c, password))):
    count = 1 if password[int(i) - 1] == c else 0
    count = count + (1 if password[int(j) - 1] == c else 0)

    return count == 1

with open(sys.argv[1], 'r') as f:
    xs = [pattern.match(l).groups() for l in f.readlines()]
    valid_1 = [x[3] for x in xs if valid_1(x)]
    valid_2 = [x[3] for x in xs if valid_2(x)]

print(len(valid_1))
print(len(valid_2))
