from collections import Counter
import fileinput


sequence = [int(l.rstrip()) for l in fileinput.input()]
sequence = [0] + sorted(sequence) + [max(sequence) + 3]

counts = Counter(b - a for a, b in zip(sequence, sequence[1:]))
print(counts[1] * counts[3])
