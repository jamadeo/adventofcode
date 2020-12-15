import fileinput
from itertools import zip_longest


def size(mask):
    if mask is None:
        return 0
    return 2 ** sum(1 for c in mask if c == 'X')


def intersection(a, b):
    assert len(a) == len(b)
    ixn = []
    for d_a, d_b in zip(a, b):
        if d_a == d_b:
            ixn.append(d_a)
        elif d_a == 'X':
            ixn.append(d_b)
        elif d_b == 'X':
            ixn.append(d_a)
        else:
            return None
    return ''.join(ixn)


def combine(mask, val):
    """Combine a mask with a value"""
    val_mask = f'{val:b}'
    combined = []
    for mask_c, val_c in zip_longest(reversed(mask), reversed(val_mask), fillvalue='0'):
        if mask_c == '0':
            combined.append(val_c)
        else:
            combined.append(mask_c)
    return ''.join(reversed(combined))


if __name__ == '__main__':
    memory = []

    running_sum = 0
    for line in fileinput.input():
        cmd, val = line.rstrip().split(' = ')
        if cmd == 'mask':
            mask = val
        else:
            val = int(val)
            mem_addr = int(cmd[4:-1])
            m = combine(mask, mem_addr)
            running_sum += size(m) * val
            memory.append((m, val))

    print(running_sum)

    from pprint import pprint
    pprint(memory)

    later_masks = []
    for mask, value in reversed(memory):
        if later_masks:
            running_sum -= total_intersection(mask, later_masks) * value
        later_masks.append(mask)

    print(running_sum)
