# -*- coding: UTF-8
import sys

def count(lines, i):
    zeroes = 0
    ones = 0
    for l in lines:
        if l[i] == '0':
            zeroes += 1
        else:
            ones += 1

    return [zeroes, ones]

def most_common_char(c):
    return '0' if c[0] > c[1] else '1'


def least_common_char(c):
    return '0' if c[0] <= c[1] else '1'

def part1(lines):
    most_common = [most_common_char(count(lines, i)) for i in range(len(lines[0]) - 1)]
    gamma = int(''.join(most_common), 2)
    epsilon = int(''.join(['1' if c == '0' else '0' for c in most_common]), 2)

    print(gamma, epsilon, gamma * epsilon)

def part2(lines):
    def filter(lines, condition):
        og_lines = lines
        bit = 0
        while len(og_lines) > 1:            
            filter_bit = condition(count(og_lines, bit))
            og_lines = [l for l in og_lines if l[bit] == filter_bit]
            bit += 1

        return og_lines[0]

    og_rating = int(filter(lines, most_common_char), 2)
    co2_rating = int(filter(lines, least_common_char), 2)

    print(og_rating, co2_rating, og_rating * co2_rating)

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    part1(lines)
    part2(lines)
    