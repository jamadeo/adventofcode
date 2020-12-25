from itertools import count
import sys


card_key = int(sys.argv[1])
door_key = int(sys.argv[2])


def transform(subject, loop_size):
    n = subject
    for i in range(loop_size-1):
        n *= subject
        n %= 20201227
    return n


def loop_size(subject, key):
    n = subject
    for i in count(2):
        n *= subject
        n %= 20201227
        if n == key:
            return i


loop_size_card = loop_size(7, card_key)
loop_size_door = loop_size(7, door_key)

print(f'{loop_size_card=}')
print(f'{loop_size_door=}')

encryption_key = transform(card_key, loop_size_door)

print(f'{encryption_key}')
