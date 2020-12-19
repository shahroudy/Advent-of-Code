import re
from collections import *
from itertools import *
from myutils.file_reader import *

MAX_REPEAT = 10


class MonsterMessages:
    def __init__(self, filename):
        groups = read_line_groups(filename)
        self.rules = groups[0]
        self.lines = groups[1]

    def parse_rules(self, mode: int):
        self.regex = defaultdict(str)
        while not self.regex[0]:
            if mode == 2:
                if self.regex[42]:
                    self.regex[8] = f'({self.regex[42]}+)'
                    if self.regex[31]:
                        r11 = str()
                        for i in range(MAX_REPEAT):
                            istr = '{'+str(i+1)+'}'
                            r11 += \
                                self.regex[42] + \
                                istr + \
                                self.regex[31] + \
                                istr + \
                                '|'
                        self.regex[11] = '(' + r11[:-1] + ')'
            for line in self.rules:
                sides = line.split(':')
                n = int(sides[0])
                if self.regex[n]:
                    continue
                rhs = sides[1].strip()
                if rhs[0] == '"':
                    self.regex[n] = re.sub('"', '', rhs)
                    continue
                terms = sides[1].split('|')
                is_ready = True
                regx = '('
                for term in terms:
                    factors = term.strip().split(' ')
                    for factor in factors:
                        factor = int(factor.strip())
                        if self.regex[factor]:
                            regx += self.regex[factor]
                        else:
                            is_ready = False
                            break
                    if is_ready:
                        regx += '|'
                    else:
                        continue
                if is_ready:
                    if len(terms) > 1:
                        self.regex[n] = regx[:-1]+')'
                    else:
                        self.regex[n] = regx[1:-1]

    def count_valid_lines(self, mode: int):
        self.parse_rules(mode)
        regex = re.compile('^'+self.regex[0]+'$')
        c = 0
        for line in self.lines:
            if regex.match(line):
                c += 1
        return c


if __name__ == '__main__':
    test1 = MonsterMessages('test1.txt')
    assert test1.count_valid_lines(1) == 2
    test2 = MonsterMessages('test2.txt')
    assert test2.count_valid_lines(1) == 3
    assert test2.count_valid_lines(2) == 12

    monster = MonsterMessages('input.txt')
    print(monster.count_valid_lines(1))
    print(monster.count_valid_lines(2))
