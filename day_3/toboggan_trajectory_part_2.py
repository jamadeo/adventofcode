import fileinput
import math


grid = [l.strip() for l in fileinput.input()]


def walk(grid, right, down):
    width = len(grid[0])
    for step, row in enumerate(grid[::down]):
        yield row[step * right % width]


def count(grid, right, down):
    return sum(1 for value in walk(grid, right, down) if value == '#')


print(math.prod(count(grid, right, down) for right, down in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))))
