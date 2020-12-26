import re
from collections import defaultdict
from myutils.file_reader import read_lines
from myutils.factorization import Factorization


class NBody:
    def __init__(self, filename):
        self.lines = read_lines(filename)

    def reset(self):
        self.positions = []
        self.velocities = []
        line_re = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
        for line in self.lines:
            parse = line_re.match(line)
            if not parse:
                raise Exception('Cannot parse the input line: ', line)
            self.positions.append([int(parse.group(i)) for i in range(1, 4)])
            self.velocities.append([0, 0, 0])

    def step_motion(self):
        for moon, position in enumerate(self.positions):
            for other_moon, other_position in enumerate(self.positions):
                if moon == other_moon:
                    continue
                for dim in range(3):
                    d = other_position[dim] - position[dim]
                    d = d//abs(d) if d else 0
                    self.velocities[moon][dim] += d
        for moon, velocity in enumerate(self.velocities):
            for dim in range(3):
                self.positions[moon][dim] += velocity[dim]

    def total_energy(self):
        total = 0
        for position, velocity in zip(self.positions, self.velocities):
            potential = sum([abs(x) for x in position])
            kinetic = sum([abs(x) for x in velocity])
            total += potential * kinetic
        return total

    def simulate(self, steps: int):
        self.reset()
        for _ in range(steps):
            self.step_motion()
        return self.total_energy()

    def find_cycle(self):
        histx = defaultdict(int)
        histy = defaultdict(int)
        histz = defaultdict(int)
        xc = yc = zc = 0

        self.reset()
        step = 1
        while not (xc and yc and zc):
            confx = tuple([p[0] for p in self.positions + self.velocities])
            confy = tuple([p[1] for p in self.positions + self.velocities])
            confz = tuple([p[2] for p in self.positions + self.velocities])
            if not xc:
                if histx[confx] > 0:
                    xc = step - histx[confx]
                else:
                    histx[confx] = step
            if not yc:
                if histy[confy] > 0:
                    yc = step - histy[confy]
                else:
                    histy[confy] = step
            if not zc:
                if histz[confz] > 0:
                    zc = step - histz[confz]
                else:
                    histz[confz] = step

            self.step_motion()
            step += 1

        factors = [xc, yc, zc]
        f = Factorization(max(factors))
        return f.least_common_multiple(factors)


if __name__ == '__main__':
    test1 = NBody('test1.txt')
    assert test1.simulate(10) == 179
    assert test1.find_cycle() == 2772
    test2 = NBody('test2.txt')
    assert test2.simulate(100) == 1940
    assert test2.find_cycle() == 4686774924

    n_body = NBody('input.txt')
    print(n_body.simulate(1000))
    print(n_body.find_cycle())
