from dataclasses import dataclass
import sys


@dataclass
class ListNode:
    value: int
    next: 'ListNode' = None
    prev: 'ListNode' = None


class CupList:
    def __init__(self, starting_sequence, total_size):
        nodes = {}
        starting_sequence = list(starting_sequence)
        sequence = starting_sequence + [*range(max(starting_sequence) + 1, total_size + 1)]
        self.num_nodes = len(sequence)

        head = ListNode(sequence[0])
        nodes[sequence[0]] = head
        ptr = head
        for i, v in enumerate(sequence[1:]):
            n = ListNode(v, prev=ptr)
            nodes[v] = n
            ptr.next = n
            ptr = n
        ptr.next = head
        head.prev = ptr
        self.head = head
        self.nodes = nodes

    def pop(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        return node

    def insert_after(self, node, to_insert):
        to_insert.next = node.next
        to_insert.next.prev = to_insert
        to_insert.prev = node
        node.next = to_insert

    def play_turn(self, selected_node):
        picked = []
        for _ in range(3):
            picked.append(self.pop(selected_node.next))
        picked_values = set(p.value for p in picked)
        next_selection = selected_node.next

        destination = ((selected_node.value - 2) % self.num_nodes) + 1
        while destination in picked_values:
            destination -= 1
            destination = ((destination - 1) % self.num_nodes) + 1

        for node in reversed(picked):
            self.insert_after(self.nodes[destination], node)

        return next_selection

    def print_from(self, node, limit=25):
        ptr = node
        if self.num_nodes <= limit:
            for _ in range(limit):
                print(ptr.value, '', end='')
                ptr = ptr.next
                if ptr == node:
                    break
        else:
            for _ in range(limit // 2):
                print(ptr.value, '', end='')
                ptr = ptr.next
            print('...', end='')
            ptr = node
            seq = []
            for _ in range(limit // 2):
                ptr = ptr.prev
                seq.append(ptr.value)
            for v in reversed(seq):
                print(v, '', end='')
        print()


total_size = int(sys.argv[2])
game = CupList([int(c) for c in sys.argv[1]], total_size)
num_moves = int(sys.argv[3])

game.print_from(game.head)

node = game.head
for move in range(num_moves):
    # print(f'-- move {move + 1} --')
    # game.print_from(node)
    node = game.play_turn(node)
    # print()

print('-- final --')
game.print_from(node)

one = game.nodes[1]
print(one.next.value, one.next.next.value)
print(one.next.value * one.next.next.value)

