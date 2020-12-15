import re
from collections import defaultdict
from itertools import product
from myutils.file_reader import read_lines


class DockingData:
    def __init__(self, filename):
        self.lines = read_lines(filename)

    def reset(self):
        self.mask = [0] * 36
        self.mem = defaultdict(int)
        return

    def bit_mask(self, value):
        mask = self.mask
        bits = list(f'{value:036b}')
        out = []
        for i in range(len(mask)):
            if mask[i] == 'X':
                out.append(bits[i])
            else:
                out.append(mask[i])
        outs = ''.join(out)
        return int(outs, 2)


    def get_addresses(self, addr):
        mask = self.mask
        bits = list(f'{int(addr):036b}')
        out = []
        for i in range(len(mask)):
            if mask[i] in ['1', 'X']:
                out.append(mask[i])
            else:
                out.append(bits[i])

        outout = []
        for xcomb in product('01', repeat=out.count('X')):
            xlist = list(xcomb)
            pat = []
            for j in out:
                if j == 'X':
                    pat.append(xlist.pop())
                else:
                    pat.append(j)
            outout.append(int(''.join(pat), 2))
        return outout

    def run(self, mode):
        self.reset()
        for line in self.lines:
            parts = [p.strip() for p in line.split('=')]
            if parts[0] == 'mask':
                self.mask = parts[1]
            elif parts[0][:3].lower() == 'mem':
                left_side = parts[0]
                left_side = re.sub('mem\[','', left_side)
                addr = re.sub('\]','',left_side)
                val = int(parts[1])
                if mode == 1:
                    self.mem[addr] = self.bit_mask(val)
                elif mode == 2:
                    for a in self.get_addresses(addr):
                        self.mem[a] = val
            else:
                raise ValueError('Invalid Command')
        return sum(self.mem.values())


if __name__ == '__main__':
    test1 = DockingData('test1.txt')
    assert test1.run(mode=1) == 165
    test2 = DockingData('test2.txt')
    assert test2.run(mode=2) == 208

    dock = DockingData('input.txt')
    print(dock.run(mode=1))
    print(dock.run(mode=2))
