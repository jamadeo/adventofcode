from collections import Counter
import fileinput


def chunks(lines):
    chunk = []
    for line in lines:
        l = line.strip()
        if l == '':
            yield chunk
            chunk = []
        else:
            chunk.append(l)
    yield chunk


def count_questions(lines):
    for chunk in chunks(lines):
        need, *rest = chunk
        answers = set(need)
        for line in rest:
            needed = tuple(answers)
            for char in needed:
                if char not in line:
                    answers.remove(char)
        yield answers


print(sum(len(group) for group in count_questions(fileinput.input())))
