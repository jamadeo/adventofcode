import fileinput


def read_decks(lines):
    deck = ()
    for line in lines:
        line = line.rstrip()
        if line == '':
            yield deck
            deck = ()
        else:
            if not line.startswith('Player'):
                deck = (*deck, int(line))
    yield deck


def play_round(p1, p2):
    c1, *d1 = p1
    c2, *d2 = p2
    d1 = tuple(d1)
    d2 = tuple(d2)

    if len(d1) >= c1 and len(d2) >= c2:
        p1wins, _, _ = play_game(d1[:c1], d2[:c2])
    else:
        p1wins = c1 > c2

    if p1wins:
        d1 = (*d1, c1, c2)
    else:
        d2 = (*d2, c2, c1)

    return p1wins, d1, d2


def play_game(p1, p2):
    seen = set()
    while all((p1, p2)):
        if (p1, p2) in seen:
            return True, p1, p2
        seen.add((p1, p2))
        _, p1, p2 = play_round(p1, p2)
    return len(p1) > 0, p1, p2


def play(p1, p2):
    _, p1, p2 = play_game(p1, p2)
    winner = p1 or p2

    return sum((i + 1) * card for i, card in enumerate(reversed(winner)))


p1, p2 = read_decks(fileinput.input())
print(play(p1, p2))
