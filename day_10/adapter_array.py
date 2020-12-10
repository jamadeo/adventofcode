import fileinput


sequence = [int(l.rstrip()) for l in fileinput.input()]
sequence = [0] + sorted(sequence) + [max(sequence)]
seq_len = len(sequence)
num_paths = [0] * seq_len
num_paths[0] = 1

for i, val in enumerate(sequence):
    for offset in (1, 2, 3):
        if i + offset < seq_len and sequence[i + offset] - val <= 3:
            num_paths[i + offset] += num_paths[i]


print(sequence)
print(num_paths)
