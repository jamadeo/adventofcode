import fileinput


DEGREES_TO_DIRECTION = {
    0: 'E',
    90: 'S',
    180: 'W',
    270: 'N',
}


def rot(x, y, degrees):
    degrees = degrees % 360
    rotations = degrees // 90
    for _ in range(rotations):
        x, y = -y, x
    return x, y


def waypoint_mover(move_sequence):
    x = 10
    y = 1

    for move in move_sequence:
        typ, val_str = move[0], move[1:]
        val = int(val_str)

        if typ == 'F':
            yield x * val, y * val
        elif typ == 'N':
            y += val
        elif typ == 'S':
            y -= val
        elif typ == 'E':
            x += val
        elif typ == 'W':
            x -= val
        elif typ == 'L':
            x, y = rot(x, y, val)
        elif typ == 'R':
            x, y = rot(x, y, -val)


x, y = 0, 0
for xd, yd in waypoint_mover(l.rstrip() for l in fileinput.input()):
    x += xd
    y += yd

print(x, y)
print(abs(x) + abs(y))
