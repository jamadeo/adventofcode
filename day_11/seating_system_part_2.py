from collections import Counter
import fileinput
from itertools import product


def zeros(grid):
    y = len(grid)
    x = len(grid[0])
    return [[0] * x for _ in y]


def mark_line(origin, step, grid, counts):
    visible = 0
    x, y = origin
    x_step, y_step = step
    while True:
        try:
            value = grid[x][y]
        except IndexError:
            return
        counts[x][y] += visible
        if value == '#':
            visible = 1
        elif value == 'L':
            visible = 0


def mark_seen(grid, counts):
    height = len(grid)
    for ix, row in enumerate(grid):
        mark_line((ix, 0), (0, 1), grid, counts)
        mark_line((ix, len(row) - 1), (0, -1), grid, counts)
    for ix, _ in enumerate(grid[0]):
        mark_line((0, ix), (1, 0), grid, counts)
        mark_line((height - 1, ix), (-1, 0), grid, counts)


def count_neighbors(grid):
    occupied = zeros(grid)

    mark_seen(grid, occupied)


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
