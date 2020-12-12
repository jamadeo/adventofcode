import fileinput


DEGREES_TO_DIRECTION = {
    0: 'E',
    90: 'S',
    180: 'W',
    270: 'N',
}


def walk(move_sequence):
    x = 0
    y = 0
    deg = 0

    for move in move_sequence:
        typ, val_str = move[0], move[1:]
        val = int(val_str)

        if typ == 'F':
            typ = DEGREES_TO_DIRECTION[deg]

        if typ == 'E':
            x += val
        elif typ == 'W':
            x -= val
        elif typ == 'N':
            y += val
        elif typ == 'S':
            y -= val
        elif typ == 'R':
            deg = (deg + val) % 360
        elif typ == 'L':
            deg = (deg - val) % 360
        else:
            assert 0, typ

    return x, y


x, y = walk(l.rstrip() for l in fileinput.input())
print(x, y)
print(abs(x) + abs(y))
