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

    def calc_combinations(self, nums):
        count = 1
        for comb_size in range(0, len(nums)-2):
            for curr in list(combinations(nums[1:-1], comb_size)):
                curr_list = list(curr)
                curr_list.extend([nums[0], nums[-1]])
                valid = True
                comb_sorted = sorted(curr_list)
                for j in range(len(comb_sorted)-1):
                    if comb_sorted[j+1] - comb_sorted[j] > 3:
                        valid = False
                        break
                if valid:
                    count += 1
        return count

    def calc_overall_combinations(self):
        s = [0] + sorted(self.nums)
        c = 1
        nums = [0]
        for i in range(len(s)-1):
            d = s[i+1]-s[i]
            if d == 3:
                c *= self.calc_combinations(nums)
                nums = [s[i+1]]
            else:
                nums.append(s[i+1])
        if len(nums):
            nums.append(nums[-1]+3)
            c *= self.calc_combinations(nums)
        return c


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
