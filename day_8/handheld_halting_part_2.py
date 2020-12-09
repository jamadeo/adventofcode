import fileinput


def read_program(lines):
    def split_line(line):
        op, n = line.rstrip().split(' ')
        return op, int(n)
    return [split_line(l) for l in lines]


def traverse(graph, start=0):
    graph_len = len(graph)
    stack = [start]
    seen = set()
    while stack:
        ix = stack.pop()
        if ix in seen:
            continue
        seen.add(ix)
        if ix < graph_len:
            yield ix
            stack.extend(graph[ix])


def build_graph(program):
    program_len = len(program)

    def offset(op, val):
        return val if op == 'jmp' else 1

    outgoing_edges = [[ix + offset(op, val)] for ix, (op, val) in enumerate(program)]
    incoming_edges = [[] for _ in range(program_len)]

    for ix, dst in enumerate(outgoing_edges):
        if dst[0] < program_len:
            incoming_edges[dst[0]].append(ix)

    return outgoing_edges, incoming_edges


def get_possible_change_coords(graph, program):
    for ix in traverse(graph):
        op, val = program[ix]
        if op == 'jmp':
            yield ix + 1, ix
        elif op == 'nop':
            yield ix + val, ix


def search_for(graph, destinations):
    for coord in traverse(graph, start=len(graph) - 1):
        if coord in destinations:
            return coord


def run_program_and_get_acc(graph):
    acc = 0
    for ix in traverse(graph):
        op, val = program[ix]
        if op == 'acc':
            acc += val
    return acc


program = read_program(fileinput.input())
outgoing_edges, incoming_edges = build_graph(program)
forks = dict(get_possible_change_coords(outgoing_edges, program))
found = forks[search_for(incoming_edges, forks)]

op, val = program[found]
program[found] = ('jmp' if op == 'nop' else 'nop', val)
outgoing_edges, incoming_edges = build_graph(program)
print(run_program_and_get_acc(outgoing_edges))
