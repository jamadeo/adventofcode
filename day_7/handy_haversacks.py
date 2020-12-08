import fileinput
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class Bag:
    color: str
    children: List[Tuple[int, 'Bag']]
    parents: List[Tuple[int, 'Bag']]


def print_graph(head, level=0, count=None):
    indent = ['\t'] * level
    st = head.color if not count else f'{head.color}[{count}]'
    print(''.join(indent), st)
    for count, child in head.children:
        print_graph(child, level+1, count=count)


def parse_rules(rules_text):
    rules = {}
    for l in rules_text:
        color, rest = l.split(sep=' bags contain ', maxsplit=1)
        contains = rest.split(', ')
        children = []
        if not contains[0].startswith('no'):
            for c in contains:
                quantity, color1, color2, *_ = c.split(' ')
                children.append((int(quantity), f'{color1} {color2}'))
        rules[color] = children
    return rules


def make_graph(rules):
    head = Bag('', [], [])
    bag_nodes = {
        color: Bag(color, [], [(0, head)]) for color in rules
    }
    head.children.extend([(None, b) for b in bag_nodes.values()])

    for parent_color, children in rules.items():
        parent_node = bag_nodes[parent_color]
        for count, child_color in children:
            child_node = bag_nodes[child_color]
            parent_node.children.append((count, child_node))
            child_node.parents.append((count, parent_node))

    return head, bag_nodes


def find_unique_ends(node):
    visited = set()
    to_visit = [(node, ())]

    while to_visit:
        ptr, path_so_far = to_visit.pop()
        if ptr.color in visited:
            continue
        visited.add(ptr.color)
        for count, parent in ptr.parents:
            if parent.color == '':  # ptr is an outermost bag
                yield ptr.color, path_so_far
            else:
                to_visit.append((parent, (ptr.color, *path_so_far)))


rules = parse_rules(fileinput.input())
head, nodes = make_graph(rules)
# print_graph(head)

print(sum(1 for color, path in find_unique_ends(nodes['shiny gold']) if path))

