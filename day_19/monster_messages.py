import fileinput


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


def matches(text, rule, all_rules):
    if not text:
        return False
    rule, rule_size = rule
    if not len(text) == rule_size:
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
    def size(rule):
        if rule in sizes:
            return sizes[rule]
        if isinstance(rule, str):
            return 1
        if isinstance(rule[0], str):
            res = sum(size(rules[r]) for r in rule)
        else:
            or_sizes = [size(r) for r in rule]
            assert min(or_sizes) == max(or_sizes)
            res = or_sizes[0]
        sizes[rule] = res
        return res

    return {
        k: (v, size(v)) for k, v in rules.items()
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

for m in messages:
    match = matches(m, rules['0'], rules)
    print(m, match)
    if match:
        sum_ += 1

print(sum_)

