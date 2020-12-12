from myutils.file_reader import read_int_list


def compute(prog, noun, verb):
    prog[1] = noun
    prog[2] = verb
    i = 0
    while i < len(prog):
        op = prog[i]
        if op == 99:
            break
        a = prog[prog[i+1]]
        b = prog[prog[i+2]]
        out = prog[i+3]
        if op == 1:
            prog[out] = a + b
        elif op == 2:
            prog[out] = a * b
        else:
            print("ERROR")
        i += 4
    return prog[0]


p = read_int_list('input.txt')
print(compute(p.copy(), 12, 2))

for noun in range(100):
    for verb in range(100):
        if compute(p.copy(), noun, verb) == 19690720:
            print(100 * noun + verb)
