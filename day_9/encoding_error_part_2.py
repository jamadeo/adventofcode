import fileinput
import sys


def find_sequence(number_sequence, target):
    seq = []
    running_sum = 0

    number_iter = iter(number_sequence)

    def advance_upper():
        nonlocal running_sum
        val = next(number_iter)
        running_sum += val
        seq.append(val)

    def advance_lower():
        nonlocal running_sum
        running_sum -= seq.pop(0)

    while True:
        if len(seq) < 2:
            advance_upper()
        elif running_sum == target:
            return min(seq) + max(seq)
        elif running_sum < target or len(seq) == 2:
            advance_upper()
        else:
            advance_lower()


target = int(sys.argv[1])

print(find_sequence((int(line.rstrip()) for line in fileinput.input(sys.argv[2])), target))
