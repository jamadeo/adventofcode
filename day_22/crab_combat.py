import fileinput


def read_decks(lines):
    deck = []
    for line in lines:
        line = line.rstrip()
        if line == '':
            yield deck
            deck = []
        else:
            if not line.startswith('Player'):
                deck.append(int(line))
    yield deck


def play_round(*decks):
    assert len(decks) > 1
    draws = sorted(((deck.pop(0), deck) for deck in decks), reverse=True)
    _, winner = draws[0]
    cards, _ = zip(*draws)
    winner.extend(cards)


def play(*decks):
    while all(decks):
        play_round(*decks)

    for player, deck in enumerate(decks):
        if deck:
            return sum((i + 1) * card for i, card in enumerate(reversed(deck)))

    assert False


p1, p2 = read_decks(fileinput.input())
print(play(p1, p2))
