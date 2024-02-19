from copy import deepcopy
import pytest

from read_data_function import read_data

# ----- PART ONE -----

DIRECTIONS = {
    'R': [0,1],
    'L': [0,-1],
    'U': [-1,0],
    'D': [1,0]
}

FILL_DIRECTIONS = {
    'R': [1,0],
    'L': [-1,0],
    'U': [0,1],
    'D': [0,-1]
}


def display_grid(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))


def dig_edge(dig_instructions: list[dict], edges: list) -> list[list[str]]:
    plan_dimensions = {
        0: {
            'min': 0,
            'max': 0
        },
        1: {
            'min': 0,
            'max': 0
        }
        }
    current = [0,0]
    for instruction in dig_instructions:
        direction = DIRECTIONS[instruction['direction']]
        current = list(map(lambda a,b: a + (instruction['steps'] * b), current, direction))
        for i in range(2):
            plan_dimensions[i]['max'] = max(current[i], plan_dimensions[i]['max'])
            plan_dimensions[i]['min'] = min(current[i], plan_dimensions[i]['min'])

    lagoon_plan = [['.' for i in range(plan_dimensions[1]['max'] - plan_dimensions[1]['min'] + 1)] \
                   for j in range(plan_dimensions[0]['max'] - plan_dimensions[0]['min'] + 1)]
    
    start = [(-1)*plan_dimensions[0]['min'], (-1)*plan_dimensions[1]['min']]
    current = deepcopy(start)
    for instruction in dig_instructions:
        direction = DIRECTIONS[instruction['direction']]
        edges.append([current, instruction['direction']])
        for i in range(instruction['steps']):
            current = list(map(lambda a,b: a + b, current, direction))
            lagoon_plan[current[0]][current[1]] = '#'
            edges.append([current, instruction['direction']])

    return lagoon_plan


def is_point_on_line(edge: list, point: list[int]) -> bool:
    if edge[-1] in ['L', 'D']:
        if point[0] != edge[0]['start'][0]:
            return False
        if not ((edge['start'][1] <= point[1] <= edge['end'][1])) or \
                ((edge['end'][1] <= point[1] <= edge['start'][1])):
            return False
    else:
        if point[1] != edge[1]['start'][1]:
            return False
        if not ((edge['start'][0] <= point[0] <= edge['end'][0])) or \
                ((edge['end'][0] <= point[0] <= edge['start'][0])):
            return False
    return True


def are_edges_partially_opposing(edge_1: list, edge_2: list) -> bool:
    if (edge_1[-1] in ['U', 'D']) and (edge_2[-1] not in ['U', 'D']):
        return False
    if (edge_1[-1] in ['L', 'R']) and (edge_2[-1] not in ['L', 'R']):
        return False

    if edge_1[-1] in ['L', 'R']:
        if any([((edge_2['start'][1] <= node[1] <= edge_2['end'][1])) or \
                ((edge_2['end'][1] <= node[1] <= edge_2['start'][1])) for node in edge_1.values()]):
            return True
    else:
        if any([((edge_2['start'][0] <= node[0] <= edge_2['end'][0])) or \
                ((edge_2['end'][0] <= node[0] <= edge_2['start'][0])) for node in edge_1.values()]):
            return True
    
    return False


def get_fill_orientation(lagoon_plan: list[list[str]], edges: list[list]):
    current = [0,0]
    edge_coords = [edge[0] for edge in edges]
    while [edge for edge in edge_coords if is_point_on_line(edge, current)] == []:
        current[0] += 1
        current[1] += 1
    edge = [edge for edge in edge_coords if is_point_on_line(edge, current)][0]
    if edge[-1] in ['L', 'D']:
        return -1
    return 1


def fill_lagoon(dig_instructions: list[dict], edges: list[list], fill_orientation: int):
    for edge in edges:
        fill_direction = [fill_orientation * num for num in FILL_DIRECTIONS[edge[1]]]
        index = [i for i in range(2) if fill_direction[i] != 0][0]
        possibly_opposing = [edge_1 for edge_1 in edges if (edge_1 != edge) and (edge[0]['start'][index] == edge[0]['start'][index])]
        while fill_spot not in edge_coords:
            lagoon_plan[fill_spot[0]][fill_spot[1]] = '#'
            fill_spot = list(map(lambda a,b: a + b, fill_spot, fill_direction))


def part_one(str_input: str):
    instructions = [{
        'direction': line.split()[0],
        'steps': int(line.split()[1]),
        'colour': line.split()[2].lstrip('(').rstrip(')')
        } for line in str_input.split('\n')]
    edges = []
    lagoon_plan = dig_edge(instructions, edges)
    fill_orientation = get_fill_orientation(lagoon_plan, edges)
    fill_lagoon(instructions, lagoon_plan, edges, fill_orientation)
    return sum([sum([1 for cell in row if cell == '#']) for row in lagoon_plan])


def test_part_one():
    assert part_one("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""") == 62


# ----- PART TWO -----

def parse_instructions(hexadecimals: list[str]) -> list[dict]:
    instructions = []
    coded_directions = {
        0: 'R',
        1: 'D',
        2: 'L',
        3: 'U'
        }
    for instruction in hexadecimals:
        direction = coded_directions[int(instruction[-1])]
        steps = int(instruction[1:-1], 16)
        instructions.append({
            'direction': direction,
            'steps': steps
        })
    return instructions
    

def dig_edge_v2(dig_instructions: list[dict]) -> list[list]:
    plan_dimensions = {
        0: {
            'min': 0,
            'max': 0
        },
        1: {
            'min': 0,
            'max': 0
        }
        }
    current = [0,0]
    for instruction in dig_instructions:
        direction = DIRECTIONS[instruction['direction']]
        current = list(map(lambda a,b: a + (instruction['steps'] * b), current, direction))
        for i in range(2):
            plan_dimensions[i]['max'] = max(current[i], plan_dimensions[i]['max'])
            plan_dimensions[i]['min'] = min(current[i], plan_dimensions[i]['min'])
    
    start = [(-1)*plan_dimensions[0]['min'], (-1)*plan_dimensions[1]['min']]
    corners = [start]
    current = deepcopy(start)
    for instruction in dig_instructions:
        direction = DIRECTIONS[instruction['direction']]
        corners.append(list(map(lambda a,b: a + (instruction['steps'] * b), current, direction)))

    return corners


def part_two(str_input: str):
    instructions = parse_instructions([line.split()[-1].lstrip('(').rstrip(')') for line in str_input.split('\n')])
    edges = dig_edge_v2(instructions)
    fill_orientation = get_fill_orientation(edges)
    fill_lagoon(instructions, edges, fill_orientation)
    return sum([sum([1 for cell in row if cell == '#']) for row in lagoon_plan])

def test_part_two():
    assert part_two("""""") == None


# --------------------


if __name__ == "__main__":
    #print(part_one(read_data("day_18.txt")))
    print(part_two(read_data("day_18.txt")))