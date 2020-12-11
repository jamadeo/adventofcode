from collections import Counter
import fileinput
from itertools import product


def point_in_grid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def zeros(grid):
    x = len(grid[0])
    return [[0] * x for _ in grid]


def mark_line(origin, step, grid, counts):
    visible = 0
    x, y = origin
    x_step, y_step = step
    while True:
        if not point_in_grid(x, y, grid):
            break
        value = grid[x][y]
        counts[x][y] += visible
        if value == '#':
            visible = 1
        elif value == 'L':
            visible = 0
        x += x_step
        y += y_step


def boundary_points(grid):
    w = len(grid)
    h = len(grid[0])

    for i in range(0, w):
        yield (i, 0)
        yield (i, h - 1)
    for i in range(1, h - 1):
        yield (0, i)
        yield (w - 1, i)


def mark_seen(grid, counts):
    for origin in boundary_points(grid):
        for step in product((-1, 0, 1), repeat=2):
            if step == (0, 0):
                continue
            xo, yo = origin
            xs, ys = step
            if not point_in_grid(xo - xs, yo - ys, grid):
                mark_line(origin, step, grid, counts)


def count_neighbors(grid):
    occupied = zeros(grid)
    mark_seen(grid, occupied)
    return occupied


def next_grid(grid):
    did_change = False
    counts = Counter()
    next_grid = []
    visible_counts = count_neighbors(grid)

    for x, row in enumerate(grid):
        next_row = []
        next_grid.append(next_row)
        for y, val in enumerate(row):
            if val == '.':
                next_val = val
            elif visible_counts[x][y] >= 5:
                next_val = 'L'
            elif visible_counts[x][y] == 0:
                next_val = '#'
            else:
                next_val = val
            next_row.append(next_val)
            did_change = did_change or next_val != val
            counts[next_val] += 1
    return next_grid, did_change, counts


def print_grid(grid):
    for row in grid:
        print(''.join(str(c) for c in row))
    print()

seating_plan = [list(line.rstrip()) for line in fileinput.input()]

while True:
    seating_plan, did_change, counts = next_grid(seating_plan)
    if not did_change:
        print(counts['#'])
        break
