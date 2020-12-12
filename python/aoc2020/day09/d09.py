from myutils.file_reader import read_int_list


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
                for k in range(j+1, i):
                    if self.nums[j] + self.nums[k] == self.nums[i]:
                        found = True
                        break
            if not found:
                return self.nums[i]
            i+=1

    def find_weakness_brute_force(self, sum):
        for i in range(len(self.nums)):
            j = i
            s = 0
            while s < sum and j < len(self.nums):
                s += self.nums[j]
                j += 1
            if s == sum:
                nums = self.nums[i:j]
                return min(nums) + max(nums)

    def find_weakness(self, sum):
        for i in range(self.count):
            j = self.int_lookup.get(sum + self.integral[i], None)
            if j is not None:
                nums = self.nums[i+1:j+1]
                return min(nums) + max(nums)


if __name__ == '__main__':
    test1 = ErrorDetector('test1.txt')
    assert test1.find_invalid(5) == 127
    assert test1.find_weakness(127) == 62
    assert test1.find_weakness_brute_force(127) == 62

    detector = ErrorDetector('input.txt')
    inval = detector.find_invalid(25)
    weakness = detector.find_weakness(inval)
    print(inval, weakness)
