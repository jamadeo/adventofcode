import fileinput


_timestamp, bus_ids_str = fileinput.input()


t = 0
product = 1

for offset, b_id in enumerate(bus_ids_str.split(',')):
    if b_id == 'x':
        continue

    b_id = int(b_id)
    while (t + offset) % b_id != 0:
        t += product
    product *= b_id


print(t)
