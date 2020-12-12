import re
from collections import defaultdict
from myutils.file_reader import read_lines


class SpaceImage:
    def __init__(self, filename, w, h):
        self.lines = read_lines(filename)
        self.w = w
        self.h = h
        self.imgsz = self.w * self.h
        self.process()

    def process(self):
        self.layers = defaultdict(list)
        digs = list(map(int, list(self.lines[0])))
        for i in range(len(digs)):
            self.layers[i//self.imgsz].append(digs[i])

    def calc(self):
        minzero = self.w * self.h
        result = 0
        for layer in self.layers.values():
            zero_count = layer.count(0)
            if zero_count < minzero:
                minzero = zero_count
                result = layer.count(1) * layer.count(2)
        return result

    def draw_image(self):
        print()
        for i in range(self.imgsz):
            j = 0
            px = 2
            while px == 2:
                px = self.layers[j][i]
                j += 1
            if px == 0:
                print(' . ', end='')
            if px == 1:
                print('###', end='')
            if (i+1) % self.w == 0:
                print()
        print()
        return


if __name__ == '__main__':
    image = SpaceImage('input.txt', 25, 6)
    print(image.calc())
    image.draw_image()
