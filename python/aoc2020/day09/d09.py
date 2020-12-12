import re
from collections import *
from itertools import *
from myutils.file_reader import *


class ErrorDetector:
    def __init__(self, filename):
        self.nums = read_int_list(filename)
        self.count = len(self.nums)
        self.process()

    def process(self):
        self.integral = dict()
        self.int_lookup = dict()
        sum = 0
        for i in range(self.count):
            sum += self.nums[i]
            self.integral[i] = sum
            self.int_lookup[sum] = i

    def find_invalid(self, window):
        for i in range(window, self.count):
            found = False
            for j in range(i-window, i):
                for k in range(i-window, i):
                    if self.nums[j] + self.nums[k] == self.nums[i]:
                        found = True
                        break
            if not found:
                return self.nums[i]
            i+=1

    def find_weakness(self, sum):
        for i in range(len(self.nums)):
            j = i
            s = 0
            while s < sum and j < len(self.nums):
                s += self.nums[j]
                j = j + 1
            if s == sum:
                m = M = self.nums[i]
                for k in range(i, j):
                    m = min(m, self.nums[k])
                    M = max(M, self.nums[k])
                return m+M

        # for i in range(self.count):
        #     j = self.int_lookup.get(sum - self.integral[i], None)
        #     if j is not None:
        #         return self.integral[i+1] - self.integral[j+1]


if __name__ == '__main__':
    test1 = ErrorDetector('test1.txt')
    assert test1.find_invalid(5) == 127
    assert test1.find_weakness(127) == 62

    detector = ErrorDetector('input.txt')
    inval = detector.find_invalid(25)
    weakness = detector.find_weakness(inval)
    print(inval, weakness)
