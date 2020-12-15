from collections import defaultdict, deque
from myutils.file_reader import read_int_list


class MemoryGame:
    def __init__(self, filename):
        self.nums = read_int_list(filename)

    def reset(self):
        self.mem = defaultdict(deque)
        self.c = 0
        for n in self.nums:
            self.c += 1
            self.mem[n].append(self.c)
        self.last = self.nums[-1]

    def calc_spoken(self, turns: list):
        if turns != sorted(turns):
            raise Exception('turns must be sorted ascending')
        self.reset()
        last, c = self.last, self.c
        result = []
        while c < max(turns):
            c += 1
            mem_last = self.mem[last]
            if len(mem_last) == 1:
                last = 0
                self.mem[last].append(c)
            else:
                last = mem_last[-1] - mem_last[-2]
                self.mem[last].append(c)
            if len(self.mem[last])>2:
                self.mem[last].popleft()
            if c in turns:
                result.append(last)
            if c % 10**6 == 0:
                print(f'Processing... step {c}')
        return result


if __name__ == '__main__':
    test1 = MemoryGame('test1.txt')
    assert test1.calc_spoken([2020]) == [436]
    test2 = MemoryGame('test2.txt')
    assert test2.calc_spoken([2020]) == [1]
    test2 = MemoryGame('test3.txt')
    assert test2.calc_spoken([2020]) == [1836]

    some = MemoryGame('input.txt')
    print(some.calc_spoken([2020, 30000000]))
