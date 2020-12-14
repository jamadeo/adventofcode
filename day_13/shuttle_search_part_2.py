import fileinput


_timestamp, bus_ids_str = fileinput.input()


t = 0
product = 1

pairs = [(int(b_id), offset) for offset, b_id in enumerate(bus_ids_str.split(',')) if b_id != 'x']
pairs_sorted = sorted(pairs)

for b_id, offset in pairs_sorted:
    b_id = int(b_id)

    while (t + offset) % b_id != 0:
        t += product

    product *= b_id


print(t)
