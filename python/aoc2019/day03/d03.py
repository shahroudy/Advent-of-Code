from collections import defaultdict

board = defaultdict(int)
mindist = minsteps = -1

file = open('input.txt', 'r')

for w in range(2):
    x = y = s = 0
    codes = file.readline().strip().split(',')
    for code in codes:
        dir = code[0].lower()
        distance = int(code[1:])
        dx = dy = 0
        if dir == 'r':
            dx = 1
        elif dir == 'l':
            dx = -1
        elif dir == 'u':
            dy = 1
        elif dir == 'd':
            dy = -1
        else:
            print('ERROR')
        for i in range(distance):
            x += dx
            y += dy
            s += 1
            if w == 0:
                if board[(x, y)] == 0:
                    board[(x, y)] = s
            else:
                if board[(x, y)]:
                    manhattan = abs(x)+abs(y)
                    sumsteps = board[(x, y)] + s
                    if mindist < 0:
                        mindist = manhattan
                    else:
                        mindist = min(mindist, manhattan)
                    if minsteps < 0:
                        minsteps = sumsteps
                    else:
                        minsteps = min(minsteps, sumsteps)
file.close()
print(mindist, minsteps)
