import fileinput


def str_to_num(s, base=2, **char_values):
    value = 0
    for place, char in enumerate(reversed(s)):
        value += char_values[char] * base ** place
    return value


def str_to_id(seat_str):
    return 8 * str_to_num(seat_str[:7], F=0, B=1) + str_to_num(seat_str[7:], L=0, R=1)


max_seat_id = 0
for line in fileinput.input():
    seat_str = line.strip()
    seat_id = str_to_id(seat_str)
    max_seat_id = max(max_seat_id, seat_id)
    print(seat_str, '->', seat_id)

print('max is', max_seat_id)
