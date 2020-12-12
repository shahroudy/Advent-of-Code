from myutils.file_reader import read_lines


class GameConsole:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.reset()

    def reset(self):
        self.head = 0
        self.prog = self.lines.copy()
        self.acc = 0
        self.hist = []
        self.terminated = False
        self.completed = False

    def step(self):
        if self.head == len(self.prog):
            self.completed = True
            self.terminated = True
            return
        if self.head in self.hist:
            self.terminated = True
            return
        else:
            self.hist.append(self.head)

        command = self.prog[self.head]
        op, operand = self.parse_command(command)
        self.execute(op, operand)
        return

    def parse_command(self, command):
        parts = command.split(' ')
        op = parts[0]
        operand = int(parts[1])
        return op, operand

    def make_command(self, op, operand):
        return f'{op} {operand}'

    def execute(self, op, operand):
        if op == 'nop':
            pass
        elif op == 'acc':
            self.acc += operand
        elif op == 'jmp':
            self.head += operand
            return
        self.head += 1
        return

    def run(self):
        while not self.terminated:
            self.step()
        return self.acc

    def run_with_correction(self):
        for mod_line in range(len(self.lines)):
            self.reset()

            # modify the mod_line command
            op, operand = self.parse_command(self.prog[mod_line])
            if op == 'jmp':
                self.prog[mod_line] = self.make_command('nop', operand)
            elif op == 'nop':
                self.prog[mod_line] = self.make_command('jmp', operand)

            self.run()

            if self.completed:
                return self.acc


if __name__ == '__main__':
    test1 = GameConsole('test1.txt')
    assert test1.run() == 5
    assert test1.run_with_correction() == 8

    console = GameConsole('input.txt')
    print(console.run(),
          console.run_with_correction())
