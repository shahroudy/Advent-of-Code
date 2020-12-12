import re
from collections import *
from itertools import *
from myutils.file_reader import *


class Some:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.process()

    def process(self):
        return

    def calc1(self, input):
        return

    def calc2(self, input):
        return

    def calc3(self, input):
        return


if __name__ == '__main__':
    test1 = Some('test1.txt')
    assert test1.calc1(000) == 000
    test2 = Some('test2.txt')
    assert test2.calc2(000) == 000

    some = Some('input.txt')
    print(some.calc1(000),
          some.calc2(000))
