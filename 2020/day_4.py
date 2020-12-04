import sys
import re

line_pattern = r'(\w+):(\S+)\s+'
required_fields = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
]

def valid_height(s):
    m = re.match(r'(\d+)(\w{2})', s)
    if m:
        h = int(m.group(1))
        unit = m.group(2)
        if unit == 'cm':
            return h >=150 and h <= 193
        elif unit == 'in':
            return h >= 59 and h <= 76

    return False

def valid_color(c):
    return re.match(r'^#[0-9a-f]{6}$', c)

rules = {
    'byr': lambda s: int(s) >= 1920 and int(s) <= 2002,
    'iyr': lambda s: int(s) >= 2010 and int(s) <= 2020,
    'eyr': lambda s: int(s) >= 2020 and int(s) <= 2030,
    'hgt': valid_height,
    'hcl': valid_color,
    'ecl': lambda s: s in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'pid': lambda s: re.match('^\d{9}$', s) != None,
    'cid': lambda s: True
}

def is_valid(passport, validate_fields):
    fields = passport.keys()
    for field in required_fields:
        if not field in fields:
            return False

    if validate_fields:
        for field in fields:
            if not rules[field](passport[field]):
                return False
    
    return True


passports = []
with open(sys.argv[1], 'r') as f:
    current_passport = {}
    for l in f.readlines():
        tuples = re.findall(line_pattern, l)
        if len(tuples) > 0:
            for field, value in tuples:
                current_passport[field] = value
        else:
            passports.append(current_passport)
            current_passport = {}

if len(current_passport.keys()) > 0:
    passports.append(current_passport)

valid = [p for p in passports if is_valid(p, False)]
print(len(valid))
valid = [p for p in passports if is_valid(p, True)]
print(len(valid))
