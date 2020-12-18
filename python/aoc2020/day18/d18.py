import re
from myutils.file_reader import read_lines


class OperationOrder:
    def __init__(self, filename: str):
        self.lines = [re.sub(r'\s', '', line) for line in read_lines(filename)]

    def read_arg(self, exp, i):
        if exp[i].isnumeric():
            openn = i
            i += 1
            while i < len(exp) and exp[openn:i+1].isnumeric():
                i += 1
            return int(exp[openn:i]), i
        elif exp[i] == '(':
            openp = i
            pc = 1
            i += 1
            while pc > 0:
                if exp[i] == '(':
                    pc += 1
                if exp[i] == ')':
                    pc -= 1
                i += 1
            return self.eval_exp(exp[openp+1:i-1]), i

    def read_op(self, exp, i):
        if exp[i] in '+*':
            op = exp[i]
            i += 1
        return op, i

    def eval_exp_plain(self, inpexp):
        i = 0
        n, i = self.read_arg(inpexp, i)
        while i < len(inpexp):
            op, i = self.read_op(inpexp, i)
            m, i = self.read_arg(inpexp, i)
            if op == '+':
                n += m
            if op == '*':
                n *= m
        return n

    def eval_exp_sum_precedence(self, inpexp):
        stack = []
        i = 0
        n, i = self.read_arg(inpexp, i)
        stack.append(n)
        while i < len(inpexp):
            op, i = self.read_op(inpexp, i)
            m, i = self.read_arg(inpexp, i)
            if op == '+':
                stack.append(m + stack.pop())
            if op == '*':
                stack.append(m)
        n = 1
        for v in stack:
            n *= v
        return n

    def eval_exp(self, inexp):
        if self.mode == 1:
            return self.eval_exp_plain(inexp)
        elif self.mode == 2:
            return self.eval_exp_sum_precedence(inexp)

    def evaluate_sum_exps(self, mode: int):
        if mode in [1, 2]:
            self.mode = mode
        else:
            raise ValueError(f'Mode {mode} is not supported')

        sum = 0
        for line in self.lines:
            sum += self.eval_exp(line)
        return sum


if __name__ == '__main__':
    test1 = OperationOrder('test1.txt')
    assert test1.evaluate_sum_exps(mode=1) == 71
    assert test1.evaluate_sum_exps(mode=2) == 231
    test2 = OperationOrder('test2.txt')
    assert test2.evaluate_sum_exps(mode=1) == 51

    op_order = OperationOrder('input.txt')
    print(op_order.evaluate_sum_exps(mode=1))
    print(op_order.evaluate_sum_exps(mode=2))
