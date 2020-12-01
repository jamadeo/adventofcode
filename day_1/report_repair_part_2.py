from collections import Counter
import fileinput
from itertools import product

values = Counter(int(line.rstrip()) for line in fileinput.input())

for v1, v2 in product(values, repeat=2):
    needed = 2020 - v1 - v2
    needed_count = 4 - len(set((v1, v2, needed)))
    if values[needed] >= needed_count:
        print(v1 * v2 * needed)
        break
