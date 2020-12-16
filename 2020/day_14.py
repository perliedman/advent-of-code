import sys
from itertools import count

with open(sys.argv[1], 'r') as f:
    lines = [l.strip().split(' = ') for l in f.readlines()]

    # Part 1
    mem = {}
    m_or = m_and = 0
    for command, val in lines:
        if command == 'mask':
            m_or = int(val.replace('X', '0'), 2)
            m_and = int(val.replace('X', '1'), 2)
        elif command.startswith('mem'):
            addr = int(command[4:].strip(']'))
            val = int(val) & m_and | m_or
            mem[addr] = val
        else:
            raise Exception('Duh')

    print(sum(mem.values()))

    # Part 2
    mem = {}
    m_or = m_float = 0
    for command, val in lines:
        if command == 'mask':
            m_or = int(val.replace('X', '0'), 2)
            f_indexes = [i for c, i in zip(val, count()) if c == 'X']
            print(f_indexes)
        elif command.startswith('mem'):
            addr_str = command[4:].strip(']')
            base_addr = list("{0:036b}".format(int(addr_str) | m_or))
            print('Base-addr', ''.join(base_addr))
            for i in range(2**len(f_indexes)):
                for j, c in zip(f_indexes, count()):
                    base_addr[j] = '1' if i & (1 << c) else '0'
                addr_bin = ''.join(base_addr)
                addr = int(addr_bin, 2)
                mem[addr] = int(val)
                print('{0:3b}'.format(i), '{0:3b}'.format(c), addr_bin, val)
        else:
            raise Exception('Duh')

    print(sum(mem.values()))