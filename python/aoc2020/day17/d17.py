from collections import defaultdict
from itertools import product
from myutils.file_reader import read_lines


class ConwayCubes:
    def __init__(self, filename):
        lines = read_lines(filename)
        self.cubes2d = defaultdict(bool)
        self.height = len(lines)
        self.width = len(lines[0])
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                if ch == '#':
                    self.cubes2d[(i,j)] = True

    def iterate_and_calculate(self, dims, cycles, verbose=0):
        if dims < 2:
            raise Exception('Dimension is not supoprted!')
        cubes = defaultdict(bool)
        for key, value in self.cubes2d.items():
            dims_key = [0]*(dims-2)
            dims_key.extend(list(key))
            cubes[tuple(dims_key)] = value

        neig_variation = list(product([-1,0,1], repeat=dims))
        neig_variation.remove(tuple([0]*dims))

        for cycle in range(1, cycles+1):
            if verbose:
                print(f'cycle: {cycle}/{cycles}')
            variations = []
            for _ in range(dims-2):
                variations.append(list(range(-cycle, cycle+1)))
            variations.append(list(range(-cycle, cycle+self.height)))
            variations.append(list(range(-cycle, cycle+self.width)))
            new_cubes = cubes.copy()
            for v in product(*variations):
                active_count = 0
                for n in neig_variation:
                    nloc = [sum(x) for x in zip(v,n)]
                    active_count += cubes[tuple(nloc)]
                if cubes[v]:
                    if active_count not in [2,3]:
                        new_cubes[v] = False
                else:
                    if active_count == 3:
                        new_cubes[v] = True
            cubes = new_cubes
            if verbose > 1:
                for k in range(-cycle, cycle+1):
                    for i in range(-cycle, self.height+cycle):
                        for j in range(-cycle, self.width+cycle):
                            print('#' if cubes[(k,i,j)] else '.', end='')
                        print()
                    print('-----------')
        return sum(cubes.values())

if __name__ == '__main__':
    test1 = ConwayCubes('test1.txt')
    assert test1.iterate_and_calculate(dims=3, cycles=6) == 112
    assert test1.iterate_and_calculate(dims=4, cycles=6) == 848

    conway_cubes = ConwayCubes('input.txt')
    print(conway_cubes.iterate_and_calculate(dims=3, cycles=6))
    print(conway_cubes.iterate_and_calculate(dims=4, cycles=6))
