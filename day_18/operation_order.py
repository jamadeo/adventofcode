import fileinput
from operator import add, mul


def tokenize(expr):
    token = ''
    for char in expr:
        if char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            token += char
        else:
            if token:
                try:
                    yield int(token)
                except TypeError:
                    yield token
                token = ''
            if char in ('(', ')', '+', '*'):
                yield char
    if token:
        try:
            yield int(token)
        except TypeError:
            yield token


def reduce_op(op, char, seq):
    it = iter(seq)
    res = [next(it)]
    for item in it:
        if item == char:
            res[-1] = op(res[-1], next(it))
        else:
            res.append(item)
    return res


def evaluate_simple(tokens):
    """evaluate with no parens"""
    tokens = list(tokens)
    reduced = reduce_op(mul, '*', reduce_op(add, '+', tokens))
    assert len(reduced) == 1
    return reduced[0]


def pop_to_char(stack):
    res = []
    while (char := stack.pop()) != '(':
        res.append(char)
    return reversed(res)


def evaluate(expr):
    stack = []
    for token in tokenize(expr):
        if token == ')':
            sub_expr = pop_to_char(stack)
            stack.append(evaluate_simple(sub_expr))
        else:
            stack.append(token)
    return evaluate_simple(stack)


sum_ = 0
for line in fileinput.input():
    s = evaluate(line)
    sum_ += s
    print(line, '->', s)


print(sum_)
