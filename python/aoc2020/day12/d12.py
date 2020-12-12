from myutils.file_reader import read_lines


class Navigation:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.process()

    def process(self):
        self.commands = [[line[0], int(line[1:])] for line in self.lines]

    def reset(self):
        self.x, self.y = 0, 0

    def run_command(self, op, num, mode):
        if op == 'L':
            for _ in range(num // 90):
                self.wx, self.wy = -self.wy, self.wx
        elif op == 'R':
            for _ in range(num // 90):
                self.wx, self.wy = self.wy, -self.wx
        elif op == 'F':
            self.x += self.wx * num
            self.y += self.wy * num
        else:
            if mode == 1:
                if op == 'N':
                    self.y += num
                elif op == 'S':
                    self.y -= num
                elif op == 'E':
                    self.x += num
                elif op == 'W':
                    self.x -= num
            elif mode == 2:
                if op == 'N':
                    self.wy += num
                elif op == 'S':
                    self.wy -= num
                elif op == 'E':
                    self.wx += num
                elif op == 'W':
                    self.wx -= num

    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    def evade(self, mode):
        self.reset()
        if mode == 1:
            self.wx, self.wy = 1, 0
        elif mode == 2:
            self.wx, self.wy = 10, 1
        else:
            raise ValueError(f'Invalid mode {mode}')

        for command in self.commands:
            self.run_command(*command, mode)
        return self.manhattan_distance()


if __name__ == '__main__':
    test1 = Navigation('test1.txt')
    assert test1.evade(mode=1) == 25
    assert test1.evade(mode=2) == 286

    navigation = Navigation('input.txt')
    print(navigation.evade(mode=1))
    print(navigation.evade(mode=2))
