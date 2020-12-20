import re
from collections import *
from itertools import *
from myutils.file_reader import *

# TODO: Code cleanup :D

def listtonum(s):
    s = list(s)
    n1 = int(''.join(s), 2)
    s.reverse()
    n2 = int(''.join(s), 2)
    return min(n1, n2)


gr = read_line_groups('input.txt')
# gr = read_line_groups('test1.txt')

tileedges = defaultdict(list)
edges = defaultdict(int)
tiles = dict()

for g in gr:
    tileno = int(g[0][5:-1])
    tilelist = []
    for line in g[1:]:
        line = re.sub('#', '1', line)
        line = re.sub('\.', '0', line)
        #line = list(map(int, line))
        tilelist.append(line)
    n1 = listtonum(tilelist[0])
    n2 = listtonum(tilelist[-1])
    ttt = [t[0] for t in tilelist]
    tt = [t[-1] for t in tilelist]
    n3 = listtonum([t[0] for t in tilelist])
    n4 = listtonum([t[-1] for t in tilelist])
    tileedges[tileno] = [n1, n4, n2, n3]
    edges[n1] += 1
    edges[n2] += 1
    edges[n3] += 1
    edges[n4] += 1

    tiles[tileno] = tilelist

m = 1
c1 = 0
for k, v in tileedges.items():
    cc = 0
    for n in v:
        if edges[n] == 1:
            cc += 1
    if cc == 2:
        c1 = k
        m *= k

print(m)

def fliph_img(t):
    new = []
    for r in t:
        r = r[::-1]
        new.append(r)
    return new


def fliph(tileno):
    tiles[tileno] = fliph_img(tiles[tileno])
    e = tileedges[tileno]
    tileedges[tileno] = [e[0], e[3], e[2], e[1]]


def flipv_img(t):
    t.reverse()
    return t


def flipv(tileno):
    tiles[tileno] = flipv_img(tiles[tileno])
    e = tileedges[tileno]
    tileedges[tileno] = [e[2], e[1], e[0], e[3]]


def rotate_img(t):
    new = []
    for c in range(len(t[0])):
        col = [row[c] for row in t]
        new.append(col)
    return fliph_img(new)


def rotate(tileno):
    tiles[tileno] = rotate_img(tiles[tileno])
    e = tileedges[tileno]
    tileedges[tileno] = [e[3], e[0], e[1], e[2]]


def rot_and_flip(tileno, topedge, leftedge):
    i = 0
    while True:
        topOK = False
        leftOK = False
        if topedge < 0:
            if edges[tileedges[tileno][0]] == 1:
                topOK = True
        else:
            if tileedges[tileno][0] == topedge:
                topOK = True
        if leftedge < 0:
            if edges[tileedges[tileno][-1]] == 1:
                leftOK = True
        else:
            if tileedges[tileno][-1] == leftedge:
                leftOK = True
        if topOK and leftOK:
            return
        i += 1
        if i != 4:
            rotate(tileno)
        else:
            fliph(tileno)
        if i > 8:
            raise Exception('Tile does not match here!')


imgtiles = [[c1]]
taken = {c1}
# rotate the corner tile to be top-left
rot_and_flip(c1, -1, -1)
redge = tileedges[c1][1]

# first row
while edges[redge] > 1:
    for t, ted in tileedges.items():
        if t not in taken and redge in ted:
            ct = t
            break
    rot_and_flip(ct, -1, redge)
    imgtiles[-1].append(ct)
    taken.add(ct)
    redge = tileedges[ct][1]

# all other rows
while edges[tileedges[imgtiles[-1][0]][2]] > 1:
    imgtiles.append([])
    col = 0
    redge = -1
    while redge < 0 or edges[redge] > 1:
        bedge = tileedges[imgtiles[-2][col]][2]
        ct = None
        for t, ted in tileedges.items():
            if (t not in taken) and (redge < 0 or redge in ted) and bedge in ted:
                ct = t
                break

        rot_and_flip(ct, bedge, redge)
        imgtiles[-1].append(ct)
        taken.add(ct)
        redge = tileedges[ct][1]
        col += 1

# make the full image
img = []
for row in imgtiles:
    rowimg = None
    for col in row:
        t = tiles[col]
        crop = [list(r[1:-1]) for r in t[1:-1]]
        if rowimg:
            for i, r in enumerate(crop):
                rowimg[i].extend(r)
        else:
            rowimg = crop
    img.extend(rowimg)

pattern = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   ']

matches= []
iteration = 0
while not matches:
    imgh = len(img)
    imgw = len(img[0])
    ptrh = len(pattern)
    ptrw = len(pattern[0])
    # find monsters
    for r in range(imgh-ptrh+1):
        for c in range(imgw-ptrw+1):
            match = True
            for pr in range(ptrh):
                for pc in range(ptrw):
                    if pattern[pr][pc] == '#':
                        if img[r+pr][c+pc] != '1':
                            match = False
                            break
                if not match:
                    break
            if match:
                matches.append([r,c])

    if not matches:
        iteration += 1
        if iteration > 8:
            raise Exception('Cannot find monsters!')
        if iteration != 4:
            img = rotate_img(img)
        else:
            img = fliph_img(img)


# print(matches)

# clear monsters
for match in matches:
    r, c = match
    for pr in range(ptrh):
        for pc in range(ptrw):
            if pattern[pr][pc] == '#':
                img[r+pr][c+pc] = '-1'

count = 0
for r in img:
    for c in r:
        if c == '1':
            count += 1

print(count)
