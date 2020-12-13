import fileinput
import math


timestamp, bus_ids_str = fileinput.input()
timestamp = int(timestamp)


bus_ids = [int(bid) for bid in bus_ids_str.split(',') if bid != 'x']

next_departure = [(bid * math.ceil(timestamp / bid), bid) for bid in bus_ids]
print(next_departure)

earliest_time, earliest_id = min(next_departure)
print(earliest_time, earliest_id)
print((earliest_time - timestamp) * earliest_id)
