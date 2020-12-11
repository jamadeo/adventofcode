from collections import Counter
import fileinput
from itertools import product


def neighbors(grid, x, y):
    for xoff, yoff in product((-1, 0, 1), repeat=2):
        if xoff == yoff == 0:
            continue
        if x + xoff < 0 or y + yoff < 0:
            continue
        try:
            yield grid[x + xoff][y + yoff]
        except IndexError:
            continue


def next_cell_value(grid, x, y):
    current_value = grid[x][y]
    if current_value == '.':
        return current_value

    neighbor_vals = Counter(neighbors(grid, x, y))
    if neighbor_vals['#'] == 0:
        return '#'

    if neighbor_vals['#'] >= 4:
        return 'L'

    return current_value


def next_grid(grid):
    did_change = False
    counts = Counter()
    next_grid = []
    for x, row in enumerate(grid):
        next_row = []
        next_grid.append(next_row)
        for y, val in enumerate(row):
            next_val = next_cell_value(grid, x, y)
            next_row.append(next_val)
            did_change = did_change or next_val != val
            counts[next_val] += 1
    return next_grid, did_change, counts


def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

seating_plan = [list(line.rstrip()) for line in fileinput.input()]

while True:
    seating_plan, did_change, counts = next_grid(seating_plan)
    if not did_change:
        print(counts['#'])
        break
