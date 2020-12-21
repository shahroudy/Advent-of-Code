import re
from collections import defaultdict
from myutils.file_reader import read_lines


class AllergenAssessment:
    def __init__(self, filename):
        self.parse_input_file(filename)
        self.refine_allergen_ingredients()

    def parse_input_file(self, filename):
        lines = read_lines(filename)
        self.allergen_ingredients = defaultdict(set)
        self.ingredient_count = defaultdict(int)

        for line in lines:
            sides = line.split('(')
            ingredients = sides[0].strip().split(' ')
            ingredients_set = set()
            for i in ingredients:
                self.ingredient_count[i] += 1
                ingredients_set.add(i)
            allergens = re.sub(r'contains|,|\)', '', sides[1])
            for allergen in allergens.strip().split(' '):
                if self.allergen_ingredients[allergen]:
                    self.allergen_ingredients[allergen] = \
                        self.allergen_ingredients[allergen].intersection(
                        ingredients_set)
                else:
                    self.allergen_ingredients[allergen] = ingredients_set

    def refine_allergen_ingredients(self):
        refined = False
        while not refined:
            refined = True
            for allergen, ingredients in self.allergen_ingredients.items():
                if len(ingredients) == 1:
                    ingredient = list(ingredients)[0]
                    for other_allergen in self.allergen_ingredients.keys():
                        if other_allergen != allergen:
                            self.allergen_ingredients[other_allergen]\
                                .discard(ingredient)
                else:
                    refined = False

    def count_safe_ingredients(self):
        ingredients_with_allergens = set()
        for ingredients in self.allergen_ingredients.values():
            ingredients_with_allergens.update(ingredients)

        total = 0
        for ingredient, count in self.ingredient_count.items():
            if ingredient not in ingredients_with_allergens:
                total += count

        return total

    def list_dangerous_ingredients(self):
        dangerous_tuples = []
        for allergen, ingredients in self.allergen_ingredients.items():
            ingredient = list(ingredients)[0]
            dangerous_tuples.append((allergen, ingredient))

        dangerous_tuples = sorted(dangerous_tuples, key=lambda x: x[0])
        dangerous_ingredients = [x[1] for x in dangerous_tuples]
        return ','.join(dangerous_ingredients)


if __name__ == '__main__':
    test1 = AllergenAssessment('test1.txt')
    assert test1.count_safe_ingredients() == 5
    assert test1.list_dangerous_ingredients() == 'mxmxvkd,sqjhc,fvjkl'

    allergen_assessment = AllergenAssessment('input.txt')
    print(allergen_assessment.count_safe_ingredients())
    print(allergen_assessment.list_dangerous_ingredients())
