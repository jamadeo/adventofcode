import fileinput


def steps(s):
    it = iter(s)
    for l in it:
        if l == 's' or l == 'n':
            yield f'{l}{next(it)}'
        else:
            yield l


assert list(steps('seswwe')) == ['se', 'sw', 'w', 'e']


def follow(seq):
    x, y = 0, 0
    for step in steps(seq):
        if step == 'w':
            x -= 1
        elif step == 'e':
            x += 1
        else:
            yd, xd = step
            y += 1 if yd == 'n' else -1
            even = y % 2
            if xd == 'w':
                x -= 1 if even else 0
            else:
                assert xd == 'e'
                x += 1 if not even else 0
    return x, y


assert follow('newse') == (0, 0)


def read_initial_grid(lines):
    flipped = set()
    for line in lines:
        c = follow(line.rstrip())
        if c in flipped:
            flipped.remove(c)
        else:
            flipped.add(c)
    return flipped


def neighbors(coord):
    x, y = coord
    even = y % 2
    return (
        (x + 1, y),
        (x - 1, y),
        (x + (1 if even else 0), y + 1),
        (x - (1 if not even else 0), y + 1),
        (x + (1 if even else 0), y - 1),
        (x - (1 if not even else 0), y - 1)
    )


def play_round(flipped):
    to_consider = set(flipped)
    for f in flipped:
        for n in neighbors(f):
            to_consider.add(n)

    new_flipped = set()
    for cell in to_consider:
        flipped_neighbors = sum(1 for n in neighbors(cell) if n in flipped)
        if cell in flipped:
            if flipped_neighbors in (1, 2):
                new_flipped.add(cell)
        else:
            if flipped_neighbors == 2:
                new_flipped.add(cell)

    return new_flipped


grid = read_initial_grid(fileinput.input())

for day in range(100):
    grid = play_round(grid)
    print(f'Day {day}: {len(grid)}')
