import re
from collections import defaultdict
from myutils.file_reader import read_lines


class LuggageProcessing:
    def __init__(self, filename):
        self.rules = read_lines(filename)
        self.process()

    def process(self):
        self.contained = defaultdict(set)
        self.contains = dict()

        for rule in self.rules:
            parts = re.sub('[.]', '', rule).split('contain')
            cont = defaultdict(int)
            parent = parts[0].strip()
            parent = re.sub('bags|bag', '', parent).strip()
            parts = parts[1].split(',')
            children = []
            for c in parts:
                sub = c.strip().split(' ')
                try:
                    count = int(sub[0])
                except ValueError:
                    continue
                child = ' '.join(sub[1:])
                child = re.sub('bags|bag', '', child).strip()
                cont[child] += count
                self.contained[child].update((parent,))
            self.contains[parent] = cont
        return

    def contained_count(self, name):
        bags = set()
        stack = [name]
        while stack:
            for k in self.contained[stack.pop()]:
                if k not in bags:
                    bags.update((k,))
                    stack.append(k)
        bags.discard(name)
        return(len(bags))

    def contains_count(self, name):
        counter = 1
        contents = self.contains.get(name, dict())
        for bag_name, count in contents.items():
            counter += count * self.contains_count(bag_name)
        return(counter)

    def contains_inside_count(self, name):
        return self.contains_count(name) - 1


if __name__ == '__main__':
    luggage_test1 = LuggageProcessing('test1.txt')
    assert luggage_test1.contained_count('shiny gold') == 4
    luggage_test2 = LuggageProcessing('test2.txt')
    assert luggage_test2.contains_inside_count('shiny gold') == 126

    luggage_proc = LuggageProcessing('input.txt')
    print(luggage_proc.contained_count('shiny gold'),
          luggage_proc.contains_inside_count('shiny gold'))
