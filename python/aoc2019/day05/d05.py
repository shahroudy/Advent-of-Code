from myutils.file_reader import read_int_list
from collections import deque


class IntcodeComputer:
    def __init__(self, program: list):
        self.init_program = program.copy()
        self.reset(deque())

    def reset(self, input: deque):
        self.program = self.init_program.copy()
        self.head = 0
        self.input = input
        self.output = deque()
        self.halted = False

    def read_op_code(self):
        code = self.program[self.head]
        parts = [code % 100]
        code //= 100
        for i in range(3):
            parts.append(code % 10)
            code //= 10
        return parts

    def read_one_operand(self, mode):
        self.head += 1
        operand = self.program[self.head]
        if mode == 0:
            operand = self.program[operand]
        return operand

    def read_operands(self, command):
        args = []
        arg_count = {99: 0, 1: 2, 2: 2, 3: 0, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2}
        no_args = arg_count[command[0]]
        for i in range(no_args):
            args.append(self.read_one_operand(command[i+1]))
        return args

    def write(self, address, value):
        self.program[address] = value

    def execute_command(self, command):
        op = command[0]
        args = self.read_operands(command)
        if op == 99:
            self.halted = True
            return
        elif op in [1, 2, 7, 8, 3]:
            value = 0
            if op == 1:
                value = args[0] + args[1]
            elif op == 2:
                value = args[0] * args[1]
            elif op == 7:
                value = 1 if args[0] < args[1] else 0
            elif op == 8:
                value = 1 if args[0] == args[1] else 0
            elif op == 3:
                value = self.input.popleft()
            address = self.read_one_operand(1)
            self.write(address, value)
        elif op == 4:
            self.output.append(args[0])
        elif op in [5, 6]:
            if (op == 5 and args[0] != 0) or (op == 6 and args[0] == 0):
                self.head = args[1]
                return False
        else:
            print("ERROR")
        self.head += 1

    def compute(self, input: deque):
        self.reset(input)
        while not self.halted:
            command = self.read_op_code()
            self.execute_command(command)
        return self.output

    # below code is added for day 7 usage
    def set_phase(self, phase):
        self.input.append(phase)

    def step(self, input: int):
        """
        This mode is used in day 7 code,
        it just starts with an input and stops when an output is generated,
        it will be returned with a new input later,
        this will go on till the computer halts!
        """
        self.input.append(input)
        while not (self.output or self.halted):
            command = self.read_op_code()
            self.execute_command(command)
        if self.halted:
            return None
        else:
            return self.output.pop()


if __name__ == '__main__':
    prog = read_int_list('input.txt')
    computer = IntcodeComputer(prog)
    print(computer.compute(deque([1])))
    print(computer.compute(deque([5])))
