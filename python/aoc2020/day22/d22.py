from collections import deque
from myutils.file_reader import read_line_groups


class CrabCombat:
    def __init__(self, filename):
        input_lines = read_line_groups(filename)
        self.start_deck1 = deque(map(int, input_lines[0][1:]))
        self.start_deck2 = deque(map(int, input_lines[1][1:]))

    def calc_score(self, deck):
        deck.reverse()
        total = 0
        for index, card in enumerate(deck):
            total += (index + 1) * card
        return total

    def simple_combat(self, deck1, deck2):
        while deck1 and deck2:
            card1, card2 = deck1.popleft(), deck2.popleft()
            if card1 > card2:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        return deck1, deck2, bool(deck1)

    def recursive_combat(self, deck1, deck2):
        game_history = set()
        while deck1 and deck2:
            decks_config = (tuple(deck1), tuple(deck2))
            if decks_config in game_history:
                return deck1, deck2, True
            else:
                game_history.add(decks_config)

            card1, card2 = deck1.popleft(), deck2.popleft()

            if len(deck1) >= card1 and len(deck2) >= card2:
                _, _, p1wins = self.recursive_combat(
                    deque(list(deck1)[:card1]),
                    deque(list(deck2)[:card2]))
            else:
                p1wins = card1 > card2

            if p1wins:
                deck1.extend([card1, card2])
            else:
                deck2.extend([card2, card1])
        return deck1, deck2, bool(deck1)

    def combat(self, recursive=False):
        deck1, deck2 = self.start_deck1.copy(), self.start_deck2.copy()
        if recursive:
            deck1, deck2, p1wins = self.recursive_combat(deck1, deck2)
        else:
            deck1, deck2, p1wins = self.simple_combat(deck1, deck2)
        return self.calc_score(deck1 if p1wins else deck2)


if __name__ == '__main__':
    test1 = CrabCombat('test1.txt')
    assert test1.combat() == 306
    assert test1.combat(recursive=True) == 291
    test2 = CrabCombat('test2.txt')
    assert test2.combat(recursive=True) > 0

    carb_combat = CrabCombat('input.txt')
    print(carb_combat.combat())
    print(carb_combat.combat(recursive=True))
