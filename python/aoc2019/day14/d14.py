import regex
from collections import defaultdict
from myutils.file_reader import read_lines


class SpaceStoichiometry:
    def __init__(self, filename):
        self.lines = read_lines(filename)
        self.process_rules()

    def process_rules(self):
        self.reactions = dict()
        reaction_re = regex.compile(r'(?:(\d+) (\w+)[\s,]*)+ => (\d+) (\w+)')
        for line in self.lines:
            match = reaction_re.match(line)
            product = match.captures(4)[0]
            product_count = int(match.captures(3)[0])
            elems = match.captures(2)
            elem_count = list(map(int, match.captures(1)))
            reaction = {
                'product_count': product_count,
                'elem': elems,
                'elem_count': elem_count
            }
            self.reactions[product] = reaction

        # introduce an order to the reactions
        remaining = set(self.reactions.keys())
        order = 0
        while remaining:
            for product in remaining.copy():
                ready = True
                for elem in self.reactions[product]['elem']:
                    if elem in remaining:
                        ready = False
                        break
                if ready:
                    remaining.remove(product)
                    self.reactions[product]['order'] = order
                    order += 1

    def needed_ORE_for_n_FUEL(self, n):
        needed = defaultdict(int)
        needed['FUEL'] = n
        changed = True
        while True:
            elems = []
            for elem, count in needed.items():
                if elem != 'ORE' and count > 0:
                    elems.append(elem)
            if not elems:
                break
            if not changed:
                elems_sorted = sorted(
                    elems,
                    key=lambda x: self.reactions[x]['order'],
                    reverse=True)
                needed[elems_sorted[0]] = \
                    self.reactions[elems_sorted[0]]['product_count']
            changed = False
            for elem in elems:
                reaction = self.reactions[elem]
                count = needed[elem]
                prod_count = reaction['product_count']
                units = count // prod_count
                if units > 0:
                    changed = True
                    needed[elem] -= units * prod_count
                    for ne, nc in zip(reaction['elem'],
                                      reaction['elem_count']):
                        needed[ne] += nc * units
        return needed['ORE']

    def needed_ORE_for_one_FUEL(self):
        return self.needed_ORE_for_n_FUEL(1)

    def calc_FUEL_from_1T_ORE(self):
        oneT = int(1e12)
        lower = oneT // self.needed_ORE_for_one_FUEL()
        upper = lower * 2
        while self.needed_ORE_for_n_FUEL(upper) < oneT:
            upper *= 2
        while upper - lower > 1:
            estimate = (lower + upper) // 2
            needed = self.needed_ORE_for_n_FUEL(estimate)
            if needed > oneT:
                upper = estimate
            elif needed < oneT:
                lower = estimate
            else:
                return estimate
        return lower


if __name__ == '__main__':
    test1 = SpaceStoichiometry('test1.txt')
    assert test1.needed_ORE_for_one_FUEL() == 165
    test2 = SpaceStoichiometry('test2.txt')
    assert test2.needed_ORE_for_one_FUEL() == 13312
    assert test2.calc_FUEL_from_1T_ORE() == 82892753
    test3 = SpaceStoichiometry('test3.txt')
    assert test3.needed_ORE_for_one_FUEL() == 180697
    assert test3.calc_FUEL_from_1T_ORE() == 5586022
    test4 = SpaceStoichiometry('test4.txt')
    assert test4.needed_ORE_for_one_FUEL() == 2210736
    assert test4.calc_FUEL_from_1T_ORE() == 460664

    space_stoichiometry = SpaceStoichiometry('input.txt')
    print(space_stoichiometry.needed_ORE_for_one_FUEL())
    print(space_stoichiometry.calc_FUEL_from_1T_ORE())
