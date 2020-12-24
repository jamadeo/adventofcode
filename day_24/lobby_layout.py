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
            odd = y % 2
            if xd == 'w':
                x -= 1 if odd else 0
            else:
                assert xd == 'e'
                x += 1 if not odd else 0
    return x, y


assert follow('newse') == (0, 0)

flipped = set()

for line in fileinput.input():
    c = follow(line.rstrip())
    if c in flipped:
        flipped.remove(c)
    else:
        flipped.add(c)

print(len(flipped))
