import pytest

from read_data_function import read_data

# ----- PART ONE -----

SIDES = {
    '-': [0,1],
    '|': [1,0]
}

CORNERS = {
    'L':{
        'x': [-1,0],
        'y': [0,1]
    },
    '7': {
        'x': [1,0],
        'y': [0,-1]
    },
    'F': {
        'x': [1,0],
        'y': [0,1]
    },
    'J': {
        'x': [-1,0],
        'y': [0,-1]
    }
}


def find_s_adjacent(pipe_map: list[list[str]], s_coord: list[int]) -> list[int]:
    if pipe_map[max(0, s_coord[0] - 1)][s_coord[1]] in ['|', 'F', '7']:
        return [max(0, s_coord[0] - 1), s_coord[1]]
    
    if pipe_map[min(len(pipe_map) - 1, s_coord[0] + 1)][s_coord[1]] in ['|', 'L', 'J']:
        return [min(len(pipe_map) - 1, s_coord[0] + 1), s_coord[1]]
    
    if pipe_map[s_coord[0]][max(0, s_coord[1] - 1)] in ['-', 'F', 'L']:
        return [s_coord[0], max(0, s_coord[1] - 1)]
    
    if pipe_map[s_coord[0]][min(len(pipe_map[0]) - 1, s_coord[1] + 1)] in ['-', 'J', '7']:
        return [s_coord[1], min(len(pipe_map[0]) - 1, s_coord[1] + 1)]
    
    return None


def find_loop(pipe_map: list[list[str]]) -> list[list[int]]:
    loop = []
    for i, row in enumerate(pipe_map):
        for j, pipe in enumerate(row):
            if pipe == "S":
                loop.append([i,j])
    
    loop.append(find_s_adjacent(pipe_map, loop[-1]))
    current = pipe_map[loop[-1][0]][loop[-1][1]]
    y_change = (loop[-1][0] - loop[-2][0])
    x_change = (loop[-1][1] - loop[-2][1])
    if current in CORNERS:
        if x_change > 0:
            orientation = 'x'
        else:
            orientation = 'y'

    while current != "S":
        y_change = (loop[-1][0] - loop[-2][0])
        x_change = (loop[-1][1] - loop[-2][1])

        if current in SIDES:
            if x_change + y_change > 0:
                loop.append([sum(coord) for coord in zip(loop[-1], SIDES[current])])
            else:
                loop.append([sum(coord) for coord in zip(loop[-1], map(lambda a: -a, SIDES[current]))])
        
            if current == '-':
                orientation = 'x'
            else:
                orientation = 'y'

        else:
            loop.append([sum(coord) for coord in zip(loop[-1], CORNERS[current][orientation])])
            if orientation == 'x':
                orientation = 'y'
            else:
                orientation = 'x'
        current = pipe_map[loop[-1][0]][loop[-1][1]]
    return loop[:-1]


def part_one(str_input: str):
    pipe_map = [list(line) for line in str_input.split("\n")]
    loop = find_loop(pipe_map)

    return int(len(loop)/2)


def test_part_one():
    assert part_one("""-L|F7
7S-7|
L|7||
-L-J|
L|-JF""") == 4


# ----- PART TWO -----


def get_starting_point(loop: list[list[int]], edges: list[str]) -> list[int]:
    for edge in edges:
        if edge not in loop:
            return edge


def min_max_map(num: int, axis: str, pipe_map: list[list[str]]) -> int:
    if axis == 'x':
        return min(max(0,num), len(pipe_map[0]) - 1)
    return min(max(0,num), len(pipe_map) - 1)


def find_start(pipe_map, loop) -> list[int]:
    current = [0,0]
    while current not in loop:
        current = [current[0] + 1, current[1] + 1]
    return current


def find_anti_clockwise_direction(loop, start) -> int:
    start_index = loop.index(start)
    above = loop[(start_index + 1)%len(loop)]
    if (above[0] > start[0]) or (above[1] < start[1]):
        return 1
    else:
        return -1


def find_all_to_left(pipe_map, loop, outside_loop, pipe, step):
    current = [pipe[0]+step[0], pipe[1]+step[1]]
    while (current not in loop) and \
        (min_max_map(current[0], 'y', pipe_map) == current[0]) and \
            (min_max_map(current[1], 'x', pipe_map) == current[1]):
        if current not in outside_loop:
            outside_loop.append(current)
        current = [current[0]+step[0], current[1]+step[1]]


def part_two(str_input: str):
    corner_vectors = {
        '7': {
            '[0, -1]': [1,0],
            '[-1, 0]': [0,1]
        },
        'F': {
            '[1, 0]': [0,1],
            '[0, -1]': [-1,0]
        },
        'J': {
            '[0, 1]': [1,0],
            '[-1, 0]': [0,-1]
        },
        'L': {
            '[1, 0]': [0,-1],
            '[0, 1]': [-1,0]
        },
    }
    pipe_map = [list(line) for line in str_input.split("\n")]
    loop = find_loop(pipe_map)

    traverse_start = find_start(pipe_map, loop)
    start_index = loop.index(traverse_start)
    if find_anti_clockwise_direction(loop, traverse_start) == -1:
        loop = loop[::-1]
    loop = loop[start_index:] + loop[:start_index]

    inside_loop = []
    for i,pipe in enumerate(loop):
        j = (i - 1)%len(loop)
        if pipe[0] > loop[j][0]:
            step = [0,1]
        elif pipe[0] < loop[j][0]:
            step = [0,-1]
        elif pipe[1] > loop[j][1]:
            step = [-1,0]
        else:
            step = [1,0]
        
        find_all_to_left(pipe_map, loop, inside_loop, pipe, step)
        
        symbol = pipe_map[pipe[0]][pipe[1]]
        if symbol in CORNERS.keys():
            find_all_to_left(pipe_map, loop, inside_loop, pipe, corner_vectors[symbol][str(step)])

    return len(inside_loop)


def test_part_two():
    assert part_two(""".....
.S-7.
.|.|.
.L-J.
.....""") == 1
    assert part_two("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""") == 4
    assert part_two(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""") == 8


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_10.txt")))
    print(part_two(read_data("day_10.txt")))