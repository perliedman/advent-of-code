import re
import sys

rule_start_pattern = r'(\w+\s\w+)\sbags*\scontain\s(.*)'
sub_rules_pattern = r'((\d)+\s(\w+\s\w+)|no other)\sbags*'

def count_node(tree, x):
    def recurse(node):
        return node == x or any([recurse(child) for (n, child) in tree[node] if child])        

    return sum([1 if recurse(child) else 0 for child in tree.keys() if child != x])

def sum_contents(tree, x):
    return sum([int(n) + int(n) * sum_contents(tree, c) if n != None else 0 for n, c in tree[x]])

with open(sys.argv[1], 'r') as f:
    sentences = f.read().strip().split('.')

    colors = {}
    for s in [s for s in sentences if len(s) > 0]:
        rule_color, rest = re.search(rule_start_pattern, s).groups()
        sub_rules = [re.search(sub_rules_pattern, s).groups()[1:] for s in rest.strip().split(',')]
        colors[rule_color] = sub_rules

    print(count_node(colors, 'shiny gold'))
    print(sum_contents(colors, 'shiny gold'))