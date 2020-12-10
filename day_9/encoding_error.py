import bisect
import fileinput
import sys


class Decoder:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.buffer_sorted = []

    def consume(self, num):
        if len(self.buffer) < self.size:
            # Part of the preamble
            self.buffer.append(num)
            return True

        if not self.buffer_sorted:
            self.buffer_sorted = sorted(self.buffer)

        if not self.has_pair(num):
            return False

        self.buffer.append(num)
        to_remove = self.buffer.pop(0)

        bisect.insort(self.buffer_sorted, num)
        self.remove_from_sorted_buffer(to_remove)

        return True

    def remove_from_sorted_buffer(self, num):
        ix = bisect.bisect_left(self.buffer_sorted, num)
        self.buffer_sorted.pop(ix)

    def has_pair(self, num):
        l, r = 0, self.size - 1

        while True:
            lower, upper = self.buffer_sorted[l], self.buffer_sorted[r]
            if lower == upper:
                # Two equal numbers is not a valid option
                return False

            summed = lower + upper
            if summed == num:
                return True

            if l == r - 1:
                return False

            if summed < num:
                l += 1
            else:
                r -= 1


size = int(sys.argv[1])

decoder = Decoder(size)

for line in fileinput.input(sys.argv[2:]):
    line = line.rstrip()
    if not decoder.consume(int(line)):
        print(line)
        break
