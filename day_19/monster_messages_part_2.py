import fileinput
import math


def read_sections(lines):
    res = []
    for line in lines:
        line = line.rstrip()
        if line == '':
            yield res
            res = []
        else:
            res.append(line)
    yield res


def parse_rule(rule_text):
    if rule_text.startswith('"'):
        return rule_text[1]
    return tuple(tuple(r.split(' ')) for r in rule_text.split(' | '))


# {'0': ((('8', '11'),), inf),
#  '11': ((('42', '31'), ('42', '11', '31')), inf),
#  '8': ((('42',), ('42', '8')), inf),
def matches_0(text, all_rules, size_42, size_31):
    for num_31s in range(1, len(text) // size_31 + 1):
        for num_42s in range(num_31s + 1, len(text) // size_42 - num_31s + 1):
            print(num_42s, num_31s)
            if matches(
                    text[:num_42s * size_42],
                    (tuple(['42'] * num_42s), size_42 * num_42s),
                    all_rules
            ) and matches(
                    text[num_42s * size_42:],
                    (tuple(['31'] * num_31s), size_31 * num_31s),
                    all_rules
            ):
                return True
    return False


def matches(text, rule, all_rules):
    if not text:
        return False
    rule, rule_size = rule
    if not len(text) == rule_size:
        print('len', text, rule, rule_size)
        return False
    if isinstance(rule, str):  # "a"
        return rule == text
    if isinstance(rule[0], str):  # 4 1 5
        offset = 0
        for rule_ix in rule:
            _next_rule, next_rule_size = all_rules[rule_ix]
            if not matches(text[offset:offset+next_rule_size], all_rules[rule_ix], all_rules):
                return False
            offset += next_rule_size
        return True
    return any(
        matches(text, (r, rule_size), all_rules) for r in rule
    )


def compute_rule_sizes(rules):
    sizes = {}
    def size(rule_name, rule):
        if rule in sizes:
            return sizes[rule]
        if isinstance(rule, str):
            return 1
        if isinstance(rule[0], str):
            if rule_name in rule:
                return math.inf
            res = sum(size(r, rules[r]) for r in rule)
        else:
            or_sizes = [size(rule_name, r) for r in rule]
            assert min(or_sizes) == max(or_sizes) or max(or_sizes) == math.inf
            res = max(or_sizes)
        sizes[rule] = res
        return res

    return {
        k: (v, size(k, v)) for k, v in rules.items()
    }


def read_input(lines):
    rules, messages = read_sections(lines)
    rules = {
        l: parse_rule(r) for rule in rules for l, r in (rule.split(': '),)
    }

    return rules, messages


rules, messages = read_input(fileinput.input())
rules = compute_rule_sizes(rules)


from pprint import pprint
pprint(rules)

sum_ = 0

_, size_42 = rules['42']
_, size_31 = rules['31']
print('ss', size_42, size_31)
for m in messages:
    match = matches_0(m, rules, size_42, size_31)
    print(m, match)
    if match:
        sum_ += 1

print(sum_)

