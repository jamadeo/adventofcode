from collections import Counter
import fileinput


def count_questions(lines):
    counts = Counter()
    for line in lines:
        answers = line.strip()
        if answers == '':
            yield counts
            counts = Counter()
        else:
            counts.update(answers)
    yield counts

print(sum(len(group) for group in count_questions(fileinput.input())))
