from myutils.file_reader import read_lines
from copy import deepcopy


class SeatingSystem:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.process()

    def process(self):
        self.rows = len(self.lines)
        self.cols = len(self.lines[0])
        self.reset()

    def reset(self):
        self.seats = [list(line) for line in self.lines]

    def copy(self):
        return

    def valid_seat(self, row, col):
        return row >= 0 and col >= 0 and row < self.rows and col < self.cols

    def count_adjacent1(self, seats, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    rn = r+i
                    cn = c+j
                    if self.valid_seat(rn, cn):
                        if seats[rn][cn] == '#':
                            count += 1
        return count

    def count_adjacent2(self, seats, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    rn = r+i
                    cn = c+j
                    while self.valid_seat(rn, cn) and seats[rn][cn] == '.':
                        rn += i
                        cn += j
                    if self.valid_seat(rn, cn):
                        if seats[rn][cn] == '#':
                            count += 1
        return count

    def count_all_occupied(self):
        count = 0
        for row in self.seats:
            for seat in row:
                if seat == '#':
                    count += 1
        return count

    def print_seats(self):
        for row in self.seats:
            for s in row:
                print(s, end='')
            print()
        print()

    def calc_final_state(self, mode, log=False):
        if mode == 1:
            tolerance = 4
            adjacent_count = self.count_adjacent1
        elif mode == 2:
            tolerance = 5
            adjacent_count = self.count_adjacent2
        else:
            raise ValueError(f'Invalid Mode: {mode}')

        self.reset()
        self.new = deepcopy(self.seats)

        changed = True
        while changed:
            changed = False
            if log:
                self.print_seats()

            self.new = []
            for line in self.seats:
                self.new.append(line.copy())

            for r in range(self.rows):
                for c in range(self.cols):
                    if self.seats[r][c] == 'L' and \
                            adjacent_count(self.seats, r, c) == 0:
                        self.new[r][c] = '#'
                        changed = True
                    if self.seats[r][c] == '#' and \
                            adjacent_count(self.seats, r, c) >= tolerance:
                        self.new[r][c] = 'L'
                        changed = True
            self.seats = self.new

        return self.count_all_occupied()


if __name__ == '__main__':
    test1 = SeatingSystem('test1.txt')
    assert test1.calc_final_state(1) == 37
    assert test1.calc_final_state(2) == 26

    some = SeatingSystem('input.txt')
    print(some.calc_final_state(1))
    print(some.calc_final_state(2))
