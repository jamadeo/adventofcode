import fileinput


def is_pw_valid(password, letter, min_count, max_count):
    letter_count = sum(1 for l in password if l == letter)
    return min_count <= letter_count <= max_count


def process_line(line_text):
    header, pw = line_text.split(':')
    minmax, letter = header.split(' ')
    min_, max_ = map(int, minmax.split('-'))
    return is_pw_valid(pw.strip(), letter, min_, max_)


print(sum(int(process_line(line)) for line in fileinput.input()))
