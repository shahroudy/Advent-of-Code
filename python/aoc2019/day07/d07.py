from collections import deque
from itertools import permutations
from myutils.file_reader import read_int_list
from aoc2019.day05.d05 import IntcodeComputer


class AmplifireControl:
    def __init__(self, prog: list):
        self.program = prog

    def compute_signal(self, phases: list):
        phases.reverse()  # for pop() to work correctly
        buffer = deque([0])
        computer = IntcodeComputer(self.program)
        while phases:
            buffer.appendleft(phases.pop())
            buffer = computer.compute(buffer)
        if len(buffer) != 1:
            print("Error")
        else:
            return buffer.pop()

    def compute_signal_feedback_loop(self, phases: list):
        computers = list()
        for phase in phases:
            computer = IntcodeComputer(self.program)
            computer.set_phase(phase)
            computers.append(computer)
        buffer = 0
        output = 0
        while buffer is not None:
            for computer in computers:
                buffer = computer.step(buffer)
            if buffer is not None:
                output = buffer
        return output


if __name__ == '__main__':
    test1 = AmplifireControl(
        [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])
    assert test1.compute_signal([4, 3, 2, 1, 0]) == 43210
    test2 = AmplifireControl([3, 23, 3, 24, 1002, 24, 10, 24, 1002,
                              23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23,
                              99, 0, 0])
    assert test2.compute_signal([0, 1, 2, 3, 4]) == 54321
    test3 = AmplifireControl([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31,
                              1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31,
                              1, 32, 31, 31, 4, 31, 99, 0, 0, 0])
    assert test3.compute_signal([1, 0, 4, 3, 2]) == 65210

    test4 = AmplifireControl([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2,
                              27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005,
                              28, 6, 99, 0, 0, 5])
    assert test4.compute_signal_feedback_loop([9, 8, 7, 6, 5]) == 139629729
    test5 = AmplifireControl([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54,
                              1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54,
                              1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55,
                              1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56,
                              -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10])
    assert test5.compute_signal_feedback_loop([9, 7, 8, 5, 6]) == 18216

    prog = read_int_list('input.txt')
    controler = AmplifireControl(prog)
    max_out_signal = 0
    for p in permutations(list(range(5))):
        max_out_signal = max(max_out_signal,
                             controler.compute_signal(list(p)))
    print(max_out_signal)

    max_out_signal2 = 0
    for p in permutations(list(range(5, 10))):
        max_out_signal2 = max(max_out_signal2,
                              controler.compute_signal_feedback_loop(list(p)))
    print(max_out_signal2)
