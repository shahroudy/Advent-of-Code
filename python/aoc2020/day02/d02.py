from myutils.file_reader import read_str_list

lines = read_str_list('input.txt')
valid1 = valid2 = 0

for line in lines:
    strings = line.split(' ')
    positions = strings[0].split('-')
    minv, maxv = int(positions[0]), int(positions[1])
    char = strings[1][0]
    password = strings[2].strip()
    count = password.count(char)
    if minv <= count <= maxv:
        valid1 += 1
    pos1, pos2 = minv - 1, maxv - 1
    if (password[pos1] == char) ^ (password[pos2] == char):
        valid2 += 1

print(valid1, valid2)
