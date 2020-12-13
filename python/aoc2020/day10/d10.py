from itertools import combinations
from myutils.file_reader import read_int_list


class AdapterArray:
    def __init__(self, filename):
        self.nums = read_int_list(filename)

    def calc_jolt_diffs(self):
        s = sorted(self.nums)
        s = [0] + s
        steps = [0] * 4
        for i in range(len(s)-1):
            steps[s[i+1]-s[i]] += 1
        steps[3] += 1
        return steps[1]*steps[3]

    def calc_overall_combinations(self):
        s = [0] + sorted(self.nums)
        c = [0] * len(s)
        c[0] = 1

        for i in range(1, len(c)):
            for j in range(i-3, i):
                if j >= 0 and s[j] >= s[i] - 3:
                    c[i] += c[j]
        return c[-1]


if __name__ == '__main__':
    test1 = AdapterArray('test1.txt')
    assert test1.calc_jolt_diffs() == 35
    assert test1.calc_overall_combinations() == 8

    test2 = AdapterArray('test2.txt')
    assert test2.calc_jolt_diffs() == 220
    assert test2.calc_overall_combinations() == 19208

    some = AdapterArray('input.txt')
    print(some.calc_jolt_diffs())
    print(some.calc_overall_combinations())
