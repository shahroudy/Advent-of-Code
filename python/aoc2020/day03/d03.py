from myutils.file_reader import read_str_list


class TobogganMap:
    def __init__(self, filename):
        self.map = read_str_list(filename)

    def calc_trees(self, dx, dy):
        x = y = c = 0
        while y < len(self.map):
            row = self.map[y]
            if row[x] == '#':
                c += 1
            x = (x + dx) % len(row)
            y += dy
        return c


if __name__ == '__main__':
    tob_test = TobogganMap('test.txt')
    assert tob_test.calc_trees(1, 1) == 2
    assert tob_test.calc_trees(3, 1) == 7
    assert tob_test.calc_trees(5, 1) == 3
    assert tob_test.calc_trees(7, 1) == 4
    assert tob_test.calc_trees(1, 2) == 2

    tob_map = TobogganMap('input.txt')
    dxs = [1, 3, 5, 7, 1]
    dys = [1, 1, 1, 1, 2]
    cm = 1
    for dx, dy in zip(dxs, dys):
        c = tob_map.calc_trees(dx, dy)
        cm *= c
        print(f'{dx}, {dy}: {c}')
    print(f'Multiplication: {cm}')
