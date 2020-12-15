import fileinput
from itertools import zip_longest, combinations
from functools import lru_cache, reduce
import time


def size(mask):
    if mask is None:
        return 0
    return 2 ** sum(1 for c in mask if c == 'X')


@lru_cache
def intersection_pair(a, b):
    if a is None or b is None:
        return None
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


def intersection(*masks):
    return reduce(intersection_pair, masks)


def size_intersection_with_union(mask, others):
    """Return the intersection of 'mask' with the union of 'others'"""
    if not others:
        return 0
    ixn_size = sum(size(intersection(mask, other)) for other in others)
    for k in range(2, len(others) + 1):
        sign = -1 if k % 2 == 0 else 1
        for combination in combinations(others, k):
            ixn_size += sign * size(intersection(*combination))
    return ixn_size


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


def addresses(mask):
    x_ix = [ix for ix, l in enumerate(mask) if l == 'X']
    mask_l = list(mask)
    for n in range(2 ** len(x_ix)):
        for i, ix in enumerate(x_ix):
            mask_l[ix] = str(int(bool(1 << i & n)))
        yield ''.join(mask_l)


if __name__ == '__main__':
    memory = {}

    running_sum = 0
    for line in fileinput.input():
        cmd, val = line.rstrip().split(' = ')
        if cmd == 'mask':
            mask = val
        else:
            val = int(val)
            mem_addr = int(cmd[4:-1])
            m = combine(mask, mem_addr)
            for address in addresses(m):
                memory[address] = val

    from pprint import pprint
    pprint(memory)

    print(sum(memory.values()))
