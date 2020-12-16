import fileinput


def is_valid(value, ranges):
    return any(min_ <= value <= max_ for min_, max_ in ranges)


def sum_of_invalid(ticket):
    all_ranges = [r for _, ranges in fields for r in ranges]
    s = 0
    for value in ticket:
        if not is_valid(value, all_ranges):
            s += value
    return s


def read_sections(lines):
    section = []
    for l in lines:
        l = l.rstrip()
        if l == '':
            yield section
            section = []
        elif l.endswith(':'):
            # Ignore section headers
            continue
        else:
            section.append(l)
    if section:
        yield section


sections = read_sections(fileinput.input())
rules_text = next(sections)
fields = []
for field in rules_text:
    name, range_text = field.split(': ')
    ranges = [tuple(map(int, r.split('-'))) for r in range_text.split(' or ')]
    fields.append((name, ranges))


my_ticket_text = next(sections)
assert len(my_ticket_text) == 1, my_ticket_text
my_ticket = list(map(int, my_ticket_text[0].split(',')))

nearby_text = next(sections)
nearby_tickets = [list(map(int, line.split(','))) for line in nearby_text]


print(fields)
print(my_ticket)
print(nearby_tickets)
print(sum(sum_of_invalid(t) for t in nearby_tickets))
