def read_str_list(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.extend(line.strip().split(','))
        return lines


def read_int_list(filename):
    return [int(s) for s in read_str_list(filename)]


def read_float_list(filename):
    return [float(s) for s in read_str_list(filename)]


def read_lines(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def read_line_groups(filename):
    groups = []
    current_group = []
    with open(filename, 'r') as file:
        while True:
            full_line = file.readline()
            line = full_line.strip()
            if not line:
                groups.append(current_group)
                current_group = []
                if not full_line:
                    break
            else:
                current_group.append(line)
    return groups
