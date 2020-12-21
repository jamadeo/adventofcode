from collections import defaultdict
import fileinput
import re

LINE_PATTERN = re.compile(r'(^.*)\(contains (.*)\)$')

def read_line(line):
    match = LINE_PATTERN.match(line)
    ingredients, allergens = match.groups()
    return set(ingredients.rstrip().split(' ')), set(allergens.split(', '))


lines = [read_line(l) for l in fileinput.input()]

all_allergens = set(allergen for ingredients, allergens in lines for allergen in allergens)
all_ingredients = set(ingredient for ingredients, allergens in lines for ingredient in ingredients)

assignments = {}

for ingredients, allergens in lines:
    for allergen in allergens:
        if allergen not in assignments:
            assignments[allergen] = set(ingredients)
        else:
            assignments[allergen] &= set(ingredients)

all_assigned = {i for ingredients in assignments.values() for i in ingredients}

final_assignments = {}
while any(len(a) for a in assignments.values()):
    for allergen, ingredients in assignments.items():
        if len(ingredients) == 1:
            found_allergen = allergen
            found_ingredient, *_ = ingredients
            break
    else:
        assert False
    final_assignments[found_allergen] = found_ingredient
    del assignments[found_allergen]
    for ingredients in assignments.values():
        ingredients.discard(found_ingredient)


print(','.join(v for k, v in sorted(final_assignments.items())))
