import fileinput
from itertools import product

from ortools.sat.python import cp_model


def is_valid(value, ranges):
    return any(min_ <= value <= max_ for min_, max_ in ranges)


def is_completely_invalid(ticket):
    all_ranges = [r for _, ranges in fields for r in ranges]
    for value in ticket:
        if not is_valid(value, all_ranges):
            return True
    return False


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


class Callback(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        super().__init__(self)

    def on_solution_callback(self):
        print('got one')


def solve(tickets):
    model = cp_model.CpModel()
    num_fields = len(fields)

    assignment_vars = {}
    for col, field in product(range(num_fields), repeat=2):
        assignment_vars[(col, field)] = model.NewBoolVar(f'col_{col}_is_field_{field}')

    for i in range(num_fields):
        model.Add(sum(assignment_vars[(j, i)] for j in range(num_fields)) == 1)
        model.Add(sum(assignment_vars[(i, j)] for j in range(num_fields)) == 1)

    for ticket in tickets:
        for col_ix, ticket_field in enumerate(ticket):
            for field_ix, (name, ranges) in enumerate(fields):
                assignment_var = assignment_vars[(col_ix, field_ix)]
                range_conditions = []
                for field_min, field_max in ranges:
                    range_conditions.append(field_min <= ticket_field <= field_max)
                model.AddBoolOr(range_conditions).OnlyEnforceIf(assignment_var)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    assert status == cp_model.OPTIMAL
    assignments = [-1 for _ in range(num_fields)]
    for col, field in product(range(num_fields), repeat=2):
        if solver.Value(assignment_vars[(col, field)]):
            assignments[col] = field
    return assignments


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

valid_tickets = [t for t in nearby_tickets if not is_completely_invalid(t)]


s = 1
assignments = solve(valid_tickets)
print(assignments)
for col, field_ix in enumerate(assignments):
    if fields[field_ix][0].startswith('departure'):
        s *= my_ticket[col]

print(s)
