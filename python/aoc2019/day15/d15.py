import os
import time
from collections import defaultdict, deque
from myutils.file_reader import read_int_list
from aoc2019.day09.d09 import IntcodeComputer


class OxygenSystem:
    def __init__(self, filename):
        self.program = read_int_list(filename)

    def reset(self):
        self.computer = IntcodeComputer(self.program.copy())
        self.map = defaultdict(int)  # 0: unknown, 1: open, -1: blocked

    def display_map(self):
        minx = miny = -5
        maxx = maxy = 5
        for x, y in self.map.keys():
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        os.system('clear')
        print()
        for j in range(miny, maxy+1):
            for i in range(minx, maxx+1):
                if (i, j) == self.oxygen:
                    ch = 'O'
                elif j == self.y and i == self.x:
                    ch = 'd'
                else:
                    m = self.map[(i, j)]
                    if m > 0:
                        ch = '.'
                    elif m < 0:
                        ch = '#'
                    else:
                        ch = ' '
                print(ch, end='')
            print()
        time.sleep(0.05)

    def neighbours(self, x, y):
        return [(x+i, y+j) for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

    def moves_to(self, target):
        conn = dict()
        q = deque([target])
        while q:
            c = q.popleft()
            x, y = c
            for n in self.neighbours(x, y):
                if self.map[n] > 0 and n not in conn:
                    conn[n] = c
                    if n == (self.x, self.y):
                        q.clear()
                        break
                    q.append(n)
        result = deque()
        c = (self.x, self.y)
        while c != target:
            n = conn[c]
            if n[0] > c[0]:
                result.append(4)
            elif n[1] > c[1]:
                result.append(2)
            elif n[0] < c[0]:
                result.append(3)
            elif n[1] < c[1]:
                result.append(1)
            else:
                raise Exception('unknown move')
            c = n
        return result

    def navigate(self, display=False):
        self.reset()
        self.x = self.y = 0
        self.map[(0, 0)] = 1
        to_visit = deque([(0, 1)])  # first must see neighbor
        tape = deque()
        self.oxygen = None
        while to_visit:
            to_visit = deque([p for p in to_visit if self.map[p] == 0])
            ns = [n for n in self.neighbours(self.x, self.y)
                  if self.map[n] == 0]
            to_visit.extend(ns)
            while not tape:
                tape = self.moves_to(to_visit.pop())

            move = tape.popleft()

            output = self.computer.step(move)
            if len(output) != 1:
                raise Exception('invalid output')
            output = output[0]

            if move == 1:
                dest = (self.x, self.y-1)
            elif move == 2:
                dest = (self.x, self.y+1)
            elif move == 3:
                dest = (self.x-1, self.y)
            elif move == 4:
                dest = (self.x+1, self.y)
            else:
                raise Exception('invalid move')

            if output == 0:
                self.map[dest] = -1
            else:
                self.map[dest] = 1
                self.x, self.y = dest
                if output == 2:
                    self.oxygen = dest
            if display:
                self.display_map()
        return

    def calc_oxygen_distance(self):
        self.x, self.y = self.oxygen
        return len(self.moves_to((0, 0)))

    def calc_filling_time(self):
        q = [self.oxygen]
        self.map[self.oxygen] = 2
        t = 0
        while True:
            newq = []
            for c in q:
                for n in self.neighbours(*c):
                    if self.map[n] == 1:
                        newq.append(n)
                        self.map[n] = 2
            if newq:
                t += 1
                q = newq
            else:
                return t


if __name__ == '__main__':
    oxygen_system = OxygenSystem('input.txt')
    oxygen_system.navigate()
    print(oxygen_system.calc_oxygen_distance())
    print(oxygen_system.calc_filling_time())
