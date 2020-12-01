from collections import Counter
import fileinput


values = Counter(int(line.rstrip()) for line in fileinput.input())

for v in values:
    needed = 2020 - v
    needed_count = 2 if needed == v else 1
    if values[needed] >= needed_count:
        print(v * needed)
        break
