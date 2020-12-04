import fileinput


grid = [l.strip() for l in fileinput.input()]


def walk(grid):
    width = len(grid[0])
    for step, row in enumerate(grid):
        yield row[step * 3 % width]


print(sum(1 for value in walk(grid) if value == '#'))
