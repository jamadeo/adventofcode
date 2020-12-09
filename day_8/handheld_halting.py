import fileinput


def read_program(lines):
    def split_line(line):
        op, n = line.rstrip().split(' ')
        return op, int(n)
    return [split_line(l) for l in lines]


def run_program_to_loop(program):
    acc = 0
    ix = 0
    ran = set()
    while True:
        if ix in ran:
            return acc
        ran.add(ix)
        op, val = program[ix]
        offset = 1
        if op == 'acc':
            acc += val
        elif op == 'jmp':
            offset = val
        ix += offset


program = read_program(fileinput.input())
print(run_program_to_loop(program))
