from collections import Counter
import fileinput
from itertools import product


def neighbors(cell):
    x, y, z, w = cell
    for dx, dy, dz, dw in product((-1, 0, 1), repeat=4):
        if (dx, dy, dz, dw) == (0, 0, 0, 0):
            continue
        yield x + dx, y + dy, z + dz, w + dw


def next_cycle(active_cells):
    active_neighbor_counts = Counter()
    for active_cell in active_cells:
        for neighbor in neighbors(active_cell):
            active_neighbor_counts[neighbor] += 1

    result = set()
    for cell, active_neighbor_count in active_neighbor_counts.items():
        if active_neighbor_count == 3:
            result.add(cell)
        elif active_neighbor_count == 2 and cell in active_cells:
            result.add(cell)

    return result


def read_initial_grid(grid):
    active_cells = set()
    for row, line in enumerate(grid):
        for col, char in enumerate(line.rstrip()):
            if char == '#':
                active_cells.add((row, col, 0, 0))
    return active_cells


def generate(initial_grid):
    active_cells = read_initial_grid(initial_grid)

    while True:
        yield active_cells
        active_cells = next_cycle(active_cells)


def print_grid(active_cells):
    xs, ys, zs, ws = zip(*active_cells)
    for w in range(min(ws), max(ws) + 1):
        for z in range(min(zs), max(zs) + 1):
            print(f'z={z}, w={w}')
            for x in range(min(xs), max(xs) + 1):
                for y in range(min(ys), max(ys) + 1):
                    print('#' if (x, y, z, w) in active_cells else '.', end='')
                print()
            print()


for cycles, grid in zip(range(7), generate(fileinput.input())):
    print(f'After {cycles} cycles')
    print_grid(grid)
    print()

print(len(grid))
