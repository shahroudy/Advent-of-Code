import re
from collections import *
from itertools import *
from myutils.file_reader import *

# TODO: code cleanup and re-implementations :D

fn = 'input.txt'
#fn = 'test1.txt'
ls = read_line_groups(fn)
# rules
rules = []
for l in ls[0]:
    parts = l.split(':')
    rs = parts[1].split('or')
    cr = []
    for r in rs:
        rg = [int(x) for x in r.strip().split('-')]
        cr.append(rg)
    rules.append(cr)

your = [int(n) for n in ls[1][1].split(',')]
nearby = []
for l in ls[2][1:]:
    nearby.append([int(n) for n in l.split(',')])

def is_valid(r, n):
    for sr in r:
        if sr[0] <= n <= sr[1]:
            return True
    return False

c = 0
val_ticks = []
for nb in nearby:
    nb_valid = True
    for n in nb:
        valid = False
        for r in rules:
            if is_valid(r,n):
                valid = True
                break
        if not valid:
            c+=n
            nb_valid = False
    if nb_valid:
        val_ticks.append(nb)
print(c)

val = defaultdict(bool)
for r in range(len(rules)):
    for o in range(len(val_ticks[0])):
        isval = True
        for t in val_ticks:
            if not is_valid(rules[r], t[o]):
                isval = False
                break
        if isval:
            val[(r,o)] = True

K = []
for r in range(len(rules)):
    os = []
    for o in range(len(rules)):
        if val[(r,o)]:
            os.append(o)
    K.append([r,os])
K = sorted(K, key=lambda x:len(x[1]))

match = [-1]*len(rules)
matchords = [-1]*len(rules)
i = 0
mset = set()
while(i<len(rules)):
    k = K[i]
    r = k[0]
    mo = k[1]
    while match[i]<0 or (mo[match[i]] in mset and match[i] < len(mo)):
        match[i] += 1
    if match[i] == len(mo):
        match[i] = -1
        i -= 1
        moi = K[i][1]
        mset.remove(moi(match[i]))
    else:
        matchords[r] = mo[match[i]]
        mset.add(mo[match[i]])
        i += 1

m = 1
for i in range(6):
    m *= your[matchords[i]]

print(m)


# 23009
# 10458887314153




# class Some:
#     def __init__(self, filename):
#         self.lines = read_lines(filename)
#         self.process()

#     def process(self):
#         return

#     def calc1(self, input):
#         return

#     def calc2(self, input):
#         return

#     def calc3(self, input):
#         return


# if __name__ == '__main__':
#     test1 = Some('test1.txt')
#     assert test1.calc1(000) == 000
#     test2 = Some('test2.txt')
#     assert test2.calc2(000) == 000

#     some = Some('input.txt')
#     print(some.calc1(000),
#           some.calc2(000))
