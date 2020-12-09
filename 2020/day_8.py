import sys

def parse_instr(l):
    instr, x = l.split()
    return (instr, int(x))

def acc(state, x):
    state['acc'] = state['acc'] + x

def jmp(state, x):
    state['ip'] = state['ip'] + x - 1

def nop(_, __):
    pass

instrs = {
    'acc': acc,
    'nop': nop,
    'jmp': jmp
}

def run(pgm):
    visited = set()
    state =  {
        'acc': 0,
        'ip': 0
    }

    while True:
        curr_ip = state['ip']
        if curr_ip == len(pgm):
            return (True, state['acc'])
        elif curr_ip in visited:
            return (False, state['acc'])

        visited.add(curr_ip)
        instr, x = pgm[curr_ip]
        instrs[instr](state, x)

        state['ip'] = state['ip'] + 1


with open(sys.argv[1], 'r') as f:
    pgm = [parse_instr(l) for l in f.readlines()]

    # Part 1
    print(run(pgm)[1])

    for i in range(len(pgm)):
        instr, x = pgm[i]
        if instr == 'jmp' or instr == 'nop':
            new_instr = 'nop' if instr == 'jmp' else 'jmp'
            test_pgm = list(pgm)
            test_pgm[i] = (new_instr, x)
            valid, acc = run(test_pgm)
            if valid:
                print(acc)
