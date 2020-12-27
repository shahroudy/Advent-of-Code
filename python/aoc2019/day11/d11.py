from collections import defaultdict
from myutils.file_reader import read_int_list
from aoc2019.day09.d09 import IntcodeComputer

prog = read_int_list('input.txt')

for puzzle in [1, 2]:
    panels = defaultdict(bool)  # false is black
    ic = IntcodeComputer(prog)
    if puzzle == 2:
        panels[(0, 0)] = True
    x, y = 0, 0
    dx, dy = 0, -1

    painted = set()

    while not ic.halted:
        input = 1 if panels[(x, y)] else 0
        out = ic.step(input)
        code = out.popleft()
        move = out.popleft()
        if code == 0:
            panels[(x, y)] = False
        elif code == 1:
            panels[(x, y)] = True
        else:
            raise Exception('Invalid output code!')
        if puzzle == 1:
            painted.add((x, y))
        if move == 0:
            dx, dy = dy, -dx
        elif move == 1:
            dx, dy = -dy, dx
        x += dx
        y += dy

    if puzzle == 1:
        print(len(painted))
    else:
        minx = miny = maxx = maxy = 0
        for key in panels.keys():
            x, y = key
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)

        print()
        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                if panels[(x, y)]:
                    print('###', end='')
                else:
                    print('   ', end='')
            print()
