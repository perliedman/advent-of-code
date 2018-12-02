from sys import stdin

numbers = map(lambda x: int(x), stdin.readlines())

seen = set()
f = 0
i = 0

while True:
  f += numbers[i % len(numbers)]

  if f in seen:
    print f
    break

  seen.add(f)

  i = i + 1
