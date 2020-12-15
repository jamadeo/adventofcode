import fileinput


memory = {}


for line in fileinput.input():
    cmd, val = line.rstrip().split(' = ')
    if cmd == 'mask':
        mask_on = 0
        mask_off = (1 << 37) - 1
        for place, bit in enumerate(reversed(val)):
            if bit == 'X':
                continue
            bit = int(bit)
            if bit:
                mask_on |= 1 << place
            else:
                mask_off &= ~(1 << place)
    else:
        val = int(val)
        val |= mask_on
        val &= mask_off
        mem_addr = int(cmd[4:len(cmd)-1])
        memory[mem_addr] = val


print(sum(memory.values()))

