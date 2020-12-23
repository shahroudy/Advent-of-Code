class CrabCups:
    def __init__(self, input):
        self.cups = list(map(int, list(input)))

    def set_next_cup(self, mode):
        self.next_cup = dict()
        for i, c in enumerate(self.cups):
            self.next_cup[c] = self.cups[(i+1) % len(self.cups)]
        if mode == 1:
            self.next_cup[self.cups[-1]] = self.cups[0]
        elif mode == 2:
            cup = max(self.cups)+1
            self.next_cup[self.cups[-1]] = cup
            while cup < 10**6:
                self.next_cup[cup] = cup + 1
                cup += 1
            self.next_cup[cup] = self.cups[0]
        else:
            raise ValueError('Invalid mode')

    def play_cups(self, mode, moves=None, log=False):
        self.set_next_cup(mode)
        current = self.cups[0]
        mincup, maxcup = min(self.next_cup), max(self.next_cup)
        if not moves:
            moves = 100 if mode == 1 else 10000000
        for move in range(moves):
            if log and move % 100000 == 0:
                print('move: ', move)
            picked = []
            p = current
            for _ in range(3):
                p = self.next_cup[p]
                picked.append(p)
            destination = current - 1
            while destination < mincup or destination in picked:
                if destination < mincup:
                    destination = maxcup
                else:
                    destination -= 1
            self.next_cup[current] = self.next_cup[picked[-1]]
            temp = self.next_cup[destination]
            self.next_cup[destination] = picked[0]
            self.next_cup[picked[-1]] = temp
            current = self.next_cup[current]

        if mode == 1:
            result = str()
            current = self.next_cup[1]
            while current != 1:
                result += str(current)
                current = self.next_cup[current]
            return result
        else:
            return self.next_cup[1] * self.next_cup[self.next_cup[1]]


if __name__ == '__main__':
    test1 = CrabCups('389125467')
    assert test1.play_cups(mode=1, moves=10) == '92658374'
    assert test1.play_cups(mode=1) == '67384529'
    assert test1.play_cups(mode=2) == 149245887792

    carb_cups = CrabCups('523764819')
    print(carb_cups.play_cups(mode=1))
    print(carb_cups.play_cups(mode=2))
