import math
from collections import defaultdict, deque
from myutils.file_reader import read_lines


class MonitoringStation:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.process()

    def process(self):
        self.asteroids = []
        for j in range(len(self.lines)):
            for i in range(len(self.lines[j])):
                if self.lines[j][i] == '#':
                    self.asteroids.append([i, j])

    def list_visible_asteroid_degrees(self, cx, cy, do_sort=False):
        degs = defaultdict(deque)
        for asteroid in self.asteroids:
            x, y = asteroid
            dx, dy = x-cx, y-cy
            if dx == 0 and dy == 0:
                continue
            d = math.atan2(dy, dx)
            degs[d].append([x, y])
        if do_sort:
            for key, value in degs.items():
                new_value = \
                    sorted(value,
                           key=lambda x: pow(x[0]-cx, 2) + pow(x[1]-cy, 2))
                degs[key] = deque(new_value)
        return degs

    def calc_visible_asteroids(self, cx, cy):
        return len(self.list_visible_asteroid_degrees(cx, cy))

    def find_best_location(self):
        bestc = bestx = besty = 0
        for asteroid in self.asteroids:
            x, y = asteroid
            visible = self.calc_visible_asteroids(x, y)
            if visible > bestc:
                bestc, bestx, besty = visible, x, y
        return bestc, bestx, besty

    def find_200th_asteroid(self):
        _, bx, by = self.find_best_location()
        degs = self.list_visible_asteroid_degrees(bx, by, do_sort=True)
        degssorted = sorted(degs.keys(), key=lambda x: (
            x+math.pi/2) % (math.pi*2))
        counter = 0
        for d in degssorted:
            if len(degs[d]):
                counter += 1
                a = degs[d].popleft()
                if counter == 200:
                    x, y = a
                    return x * 100 + y


if __name__ == '__main__':
    test1 = MonitoringStation('test1.txt')
    assert test1.calc_visible_asteroids(3, 4) == 8
    assert test1.calc_visible_asteroids(4, 2) == 5
    assert test1.find_best_location() == (8, 3, 4)
    test2 = MonitoringStation('test2.txt')
    assert test2.calc_visible_asteroids(11, 13) == 210
    assert test2.find_best_location() == (210, 11, 13)
    assert test2.find_200th_asteroid() == 802

    station = MonitoringStation('input.txt')
    print(station.find_best_location())
    print(station.find_200th_asteroid())
