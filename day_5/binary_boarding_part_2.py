import fileinput


def str_to_num(s, base=2, **char_values):
    value = 0
    for place, char in enumerate(reversed(s)):
        value += char_values[char] * base ** place
    return value


def str_to_id(seat_str):
    return 8 * str_to_num(seat_str[:7], F=0, B=1) + str_to_num(seat_str[7:], L=0, R=1)


def find_my_seat(all_seat_ids):
    sorted_seats = sorted(all_seat_ids)
    for before, after in zip(sorted_seats, sorted_seats[1:]):
        if after - before == 2:
            return after - 1


seat_ids = [str_to_id(line.strip()) for line in fileinput.input()]
print(find_my_seat(seat_ids))
