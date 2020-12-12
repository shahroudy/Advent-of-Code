from collections import Counter

start = 168630
end = 718098

c1 = c2 = 0
for i in range(start, end):
    s = str(i)
    if ''.join(sorted(s)) != s:
        continue
    cnt = Counter(s)
    repeat1 = False
    for k, v in cnt.items():
        if v > 1:
            repeat1 = True
            break
    repeat2 = False
    for k, v in cnt.items():
        if v == 2:
            repeat2 = True
            break
    if repeat1:
        c1 += 1
    if repeat2:
        c2 += 1

print(c1, c2)
