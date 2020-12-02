import fileinput


def is_pw_valid(password, letter, pos1, pos2):
    return (password[pos1 - 1] == letter) ^ (password[pos2 - 1] == letter)


def process_line(line_text):
    header, pw = line_text.split(':')
    minmax, letter = header.split(' ')
    pos1, pos2 = map(int, minmax.split('-'))
    return is_pw_valid(pw.strip(), letter, pos1, pos2)


print(sum(int(process_line(line)) for line in fileinput.input()))
