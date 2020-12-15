import sys
from itertools import count


def play_game(starting_sequence):
    memory = {}

    for ix, num in enumerate(starting_sequence):
        yield num
        memory[num] = ix
        last_spoken_number = num

    for ix in count(ix + 1):
        if last_spoken_number in memory:
            next_value = ix - 1 - memory[last_spoken_number]
        else:
            next_value = 0
        yield next_value
        memory[last_spoken_number] = ix - 1
        last_spoken_number = next_value


sequence = map(int, sys.argv[1].split(','))

for num, ix in zip(play_game(sequence), range(30000000)):
    print(ix, num)



