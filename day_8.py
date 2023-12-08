import pytest
import numpy as np

from read_data_function import read_data

# ----- PART ONE -----


def traverse_nodes(start: str, destination: str, directions: list[str], node_dict: dict):
    count = 0
    current = start
    while (current != destination) or (count == 0):
        count += 1
        direction = directions[(count - 1)%len(directions)]
        if direction == 'L':
            current = node_dict[current][0]
        else:
            current = node_dict[current][1]
    return count


def part_one(str_input: str):
    directions = list(str_input.split('\n\n')[0])
    nodes = str_input.split('\n\n')[1].split('\n')
    node_dict = {}
    for node in nodes:
        node_dict[node.split(' = ')[0]] = [
            node.split(' = ')[1].split(', ')[0].lstrip('('),
            node.split(' = ')[1].split(', ')[1].rstrip(')')
            ]
    return traverse_nodes('AAA', 'ZZZ', directions, node_dict)


def test_part_one():
    assert part_one("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""") == 2


# ----- PART TWO -----


def z_list_for_node(node: str, directions: list[str], node_dict:dict) -> list[str]:
    count = 0
    z_list = []
    while node not in z_list:
        count += 1
        direction = directions[(count - 1)%len(directions)]
        if direction == 'L':
            node = node_dict[node][0]
        else:
            node = node_dict[node][1]
        if node[-1] == "Z":
            z_list.append(node)
    return z_list


def part_two(str_input: str):
    directions = list(str_input.split('\n\n')[0])
    nodes = str_input.split('\n\n')[1].split('\n')
    node_dict = {}
    for node in nodes:
        node_dict[node.split(' = ')[0]] = [
            node.split(' = ')[1].split(', ')[0].lstrip('('),
            node.split(' = ')[1].split(', ')[1].rstrip(')')
            ]
    a_nodes = [node for node in node_dict.keys() if node[-1] == "A"]
    factors_and_constants = []
    for node in a_nodes:
        z_node = z_list_for_node(node, directions, node_dict)[0]
        constant = traverse_nodes(node, z_node, directions, node_dict)
        print(len(directions))
        factors_and_constants.append({
            'constant': constant,
            'factor': traverse_nodes(z_node, z_node, directions[constant:] + directions[:constant], node_dict)
        })
    #factor always == constant, for some reason, and is always a divisor of directions, which makes it much easier
    return np.lcm.reduce([node['factor'] for node in factors_and_constants])


def test_part_two():
    assert part_two("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""") == 6


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_8.txt")))
    print(part_two(read_data("day_8.txt")))