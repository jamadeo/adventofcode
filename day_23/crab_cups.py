import sys


def roll(li, n):
    return li[n:] + li[:n]


def play_cups(cups, current_cup_ix):
    cups = roll(list(cups), current_cup_ix)
    num_cups = len(cups)

    picked_up = [cups.pop((1) % num_cups) for _ in range(3)]
    destination_cup = cups[0] - 1 or num_cups
    while destination_cup in picked_up:
        destination_cup -= 1
        if destination_cup == 0:
            destination_cup = num_cups
    destination_cup_index = cups.index(destination_cup)
    for c in reversed(picked_up):
        cups.insert(destination_cup_index + 1, c)

    return tuple(roll(cups, -current_cup_ix)), tuple(picked_up), destination_cup


def format_cups(cups, current_cup_ix):
    return ' '.join(f'({c})' if i == current_cup_ix else str(c) for i, c in enumerate(cups))


cups = [int(c) for c in sys.argv[1]]
num_moves = int(sys.argv[2])
for move in range(num_moves):
    print(f'-- move {move + 1} --')
    print('cups:', format_cups(cups, move % len(cups)))
    cups, pick_up, destination = play_cups(cups, move % len(cups))
    print('pick up:', ','.join(str(c) for c in pick_up))
    print('destination:', destination)
    print()


print('-- final --')
print('cups:', format_cups(cups, (move + 1) % len(cups)))
