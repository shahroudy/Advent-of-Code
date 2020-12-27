import os, time
from collections import defaultdict
from myutils.file_reader import read_int_list
from aoc2019.day09.d09 import IntcodeComputer


class CarePackage:
    def __init__(self, filename):
        self.program = read_int_list(filename)

    def reset(self):
        self.computer = IntcodeComputer(self.program)
        self.board = defaultdict(int)
        self.score = 0
        self.ball_x = 0
        self.paddle_x = 0

    def apply_output(self, out):
        while out:
            x, y, obj = out.popleft(), out.popleft(), out.popleft()
            if x >= 0:
                self.board[(y, x)] = obj
                if obj == 3:
                    self.paddle_x = x
                elif obj == 4:
                    self.ball_x = x
            else:
                self.score = obj

    def read_board(self):
        self.apply_output(self.computer.step())

    def play_move(self, input):
        self.apply_output(self.computer.step(input))

    def count_blocks(self):
        self.reset()
        self.read_board()
        count = 0
        for v in self.board.values():
            if v == 2:
                count += 1
        return count

    @staticmethod
    def display_char(object):
        if object == 0:
            print(' ', end='')
        elif object == 1:
            print('#', end='')
        elif object == 2:
            print('x', end='')
        elif object == 3:
            print('T', end='')
        elif object == 4:
            print('o', end='')

    def display_board(self):
        xmin = xmax = ymin = ymax = 0
        for k in self.board.keys():
            y, x = k
            xmin = min(xmin, x)
            xmax = max(xmax, x)
            ymin = min(ymin, y)
            ymax = max(ymax, y)
        os.system('clear')
        print(f'Score: {self.score}')
        for y in range(ymin, ymax+1):
            for x in range(xmin, xmax+1):
                self.display_char(self.board[(y, x)])
            print()

    def play_arcade(self, display=False):
        self.reset()
        self.read_board()
        self.computer.program[0] = 2
        self.computer.halted = False
        while not self.computer.halted:
            if display:
                self.display_board()
                time.sleep(0.04)
            diff = self.ball_x - self.paddle_x
            if diff == 0:
                input = 0
            elif diff > 0:
                input = 1
            else:
                input = -1
            self.play_move(input)
        return self.score


if __name__ == '__main__':
    care_package = CarePackage('input.txt')
    print(care_package.count_blocks())
    print(care_package.play_arcade(display=False))
