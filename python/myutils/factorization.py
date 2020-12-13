from collections import defaultdict

class Factorization:
    def __init__(self, max_num):
        self._max = max_num
        self._find_primes()

    def _find_primes(self):
        is_prime = [True] * self._max
        for i in range(2, int(self._max**0.5+1)):
            if is_prime[i]:
                for j in range(i*2, self._max, i):
                    is_prime[j] = False
        self.primes = [i for i in range(2, self._max) if is_prime[i]]

    def print_primes(self):
        print(f'Primes: {self.primes}')

    def factorize(self, num):
        factors = defaultdict(int)
        for p in self.primes:
            while num % p == 0:
                factors[p] += 1
                num //= p
            if num == 1:
                break
        return factors

    def combine_factors(self, factors):
        result = 1
        for factor, power in factors.items():
            result *= (factor ** power)
        return result

    def least_common_multiple(self, nums: list):
        factors = defaultdict(int)
        for num in nums:
            for factor, power in self.factorize(num).items():
                factors[factor] = max(factors[factor], power)
        return self.combine_factors(factors)

    def greatest_common_factor(self, nums: list):
        factors = self.factorize(nums[0])
        for num in nums[1:]:
            for factor, power in self.factorize(num).items():
                factors[factor] = min(factors[factor], power)
        return self.combine_factors(factors)

if __name__ == '__main__':
    test = Factorization(max_num=10**5)
    assert test.factorize(99) == {3:2, 11:1}
    assert test.combine_factors({3:2, 11:1}) == 99
    assert test.least_common_multiple([12,8,6]) == 24
    assert test.greatest_common_factor([50,60,70]) == 10
