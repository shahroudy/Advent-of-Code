from collections import defaultdict, deque
from myutils.file_reader import read_lines


class LobbyLayout:
    def __init__(self, filename):
        self.process(filename)

    def process(self, filename):
        lines = read_lines(filename)
        self.tiles = defaultdict(bool)  # white is False
        for line in lines:
            q = deque(line)
            x, y = 0, 0
            while q:
                d = q.popleft()
                if d in 'ns':
                    d = d + q.popleft()
                if d == 'e':
                    x += 2
                elif d == 'w':
                    x -= 2
                elif d == 'ne':
                    x += 1
                    y += 1
                elif d == 'nw':
                    x -= 1
                    y += 1
                elif d == 'se':
                    x += 1
                    y -= 1
                elif d == 'sw':
                    x -= 1
                    y -= 1
            self.tiles[(x, y)] = not self.tiles[(x, y)]

    def count_black_tiles(self):
        return sum(self.tiles.values())

    @staticmethod
    def adjacent_tiles(x, y):
        return {(x-2, y), (x+2, y),
                (x-1, y-1), (x-1, y+1),
                (x+1, y-1), (x+1, y+1)}

    def count_black_afte_flipping(self, days):
        tiles = self.tiles.copy()
        for _ in range(days):
            tilestocheck = set()
            for t in tiles.keys():
                tilestocheck.add(t)
                tilestocheck.update(self.adjacent_tiles(*t))

            newtiles = defaultdict(bool)
            for t in tilestocheck:
                black_adjacents = \
                    sum([tiles[n] for n in self.adjacent_tiles(*t)])
                if tiles[t]:
                    if black_adjacents == 0 or black_adjacents > 2:
                        newtiles[t] = False
                    else:
                        newtiles[t] = True
                else:
                    if black_adjacents == 2:
                        newtiles[t] = True
                    else:
                        newtiles[t] = False

            tiles = newtiles

        return sum(tiles.values())


if __name__ == '__main__':
    test1 = LobbyLayout('test1.txt')
    assert test1.count_black_tiles() == 10
    assert test1.count_black_afte_flipping(1) == 15
    assert test1.count_black_afte_flipping(10) == 37
    assert test1.count_black_afte_flipping(100) == 2208

    lobby_layout = LobbyLayout('input.txt')
    print(lobby_layout.count_black_tiles())
    print(lobby_layout.count_black_afte_flipping(100))
