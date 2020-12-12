from myutils.file_reader import read_int_list

lines = read_int_list('input.txt')

s = 0
s2 = 0
for n in lines:
    f = max(0, n // 3 - 2)
    s += f
    s2 += f
    while f > 0:
        f = max(0, f // 3 - 2)
        s2 += f

print(s, s2)
