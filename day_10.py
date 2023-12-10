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
        print('a')
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
OPPOSITE_DICT = {
    '7': 'F',
    'F': '7',
    'J': 'L',
    'L': 'J'
}

def get_starting_point(loop: list[list[int]], edges: list[str]) -> list[int]:
    for edge in edges:
        if edge not in loop:
            return edge


def min_max_map(num: int, axis: str, pipe_map: list[list[str]]) -> int:
    if axis == 'x':
        return min(max(0,num), len(pipe_map) - 1)
    return min(max(0,num), len(pipe_map[0]) - 1)



def follow_touching_edges(pipe_map: list[list[str]], loop: list[list[int]], o_loop: list[list[int]], edge: list[list[int]], direction: str):
    while True:
        print(edge, pipe_map[edge[-1][0]][edge[-1][1]], direction, len(o_loop))
        match direction:
            case 'up':
                orientation = 'y'
                parallel = [0,1]
            case 'down':
                orientation = 'y'
                parallel = [0,-1]
            case 'left':
                orientation = 'x'
                parallel = [-1,0]
            case 'right':
                orientation = 'x'
                parallel = [1,0]
        
        current = edge[-1]

        parallel_pipe = [min_max_map(current[0]+parallel[0], 'x', pipe_map),min_max_map(current[1]+parallel[1], 'y', pipe_map)]
        if (parallel_pipe not in loop) and (parallel_pipe not in o_loop):
            o_loop.append(parallel_pipe)
            return None
        
        symbol = pipe_map[current[0]][current[1]]

        if symbol in CORNERS.keys():
            change = CORNERS[pipe_map[current[0]][current[1]]][orientation]
            next = [min_max_map(current[0] + change[0], 'x', pipe_map), min_max_map(current[1] + change[1], 'y', pipe_map)]

            match direction:
                case 'up':
                    if symbol == '7':
                        direction = 'left'
                    elif symbol == 'F':
                        direction = 'right'
                case 'down':
                    if symbol == 'J':
                        direction = 'left'
                    elif symbol == 'L':
                        direction = 'right'
                case 'left':
                    if symbol == 'F':
                        direction = 'down'
                    elif symbol == 'L':
                        direction = 'up'
                case 'right':
                    if symbol == 'J':
                        direction = 'up'
                    elif symbol == '7':
                        direction = 'down'
            
        elif symbol == '|':
            if direction == 'down':
                next = [current[0], min_max_map(current[1] + 1, 'y', pipe_map)]
            else:
                next = [current[0], min_max_map(current[1] - 1, 'y', pipe_map)]
    
        elif symbol == '|':
            if direction == 'right':
                next = [min_max_map(current[0] + 1, 'x', pipe_map), current[1]]
            else:
                next = [min_max_map(current[0] - 1, 'x', pipe_map), current[1]]

        if next in edge:
                return None
            
        edge.append(next)


def find_adjacent(pipe_map: list[list[str]], loop: list[list[int]], o_loop: list[list[int]], index: int):
    current = o_loop[index]
    for i in range(max(current[0] - 1, 0), min(len(pipe_map), current[0] + 2)):
        for j in range(max(current[1] - 1, 0), min(len(pipe_map[0]), current[1] + 2)):
            if ([i,j] not in loop) and ([i,j] not in o_loop):
                o_loop.append([i,j])
            elif ([i,j] in loop) and (pipe_map[i][j] in ['7','F','J','L']):
                symbol = pipe_map[i][j]
                inv_symbol = OPPOSITE_DICT[symbol]
                match pipe_map[i][j]:
                    case '7':
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'right')
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'up')
                    case 'F':
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'left')
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'up')
                    case 'J':
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'down')
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'right')
                    case 'L':
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'left')
                        follow_touching_edges(pipe_map, loop, o_loop, [[i, j]], 'down')



def find_outside_loop(pipe_map: list[list[str]], loop: list[list[int]]) -> list[list[int]]:
    outside_loop = []
    edges = [[0,i] for i in range(0,len(pipe_map[0]))] + \
            [[len(pipe_map) - 1,i] for i in range(0,len(pipe_map[0]))] + \
            [[i,0] for i in range(0,len(pipe_map))] + \
            [[i,len(pipe_map[0]) - 1] for i in range(0,len(pipe_map))]
    outside_loop.append(get_starting_point(loop, edges))
    index = 0
    while index < len(outside_loop):
        find_adjacent(pipe_map, loop, outside_loop, index)
        index += 1
    return outside_loop


def find_all_to_left(pipe_map, loop, outside_loop, pipe, step):
    current = [pipe[0]+step[0], pipe[1]+step[1]]
    while (current not in loop) and \
        (min_max_map(current[0], 'x', pipe_map) == current[0]) and \
            (min_max_map(current[1], 'y', pipe_map) == current[1]):
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
            '[-1, 0]': [0,-1],
            '[0, 1]': [1,0]
        },
        'J': {
            '[0, -1]': [-1,0],
            '[1, 0]': [0,1]
        },
        'L': {
            '[1, 0]': [0,1],
            '[0, 1]': [-1,0]
        },
    }
    pipe_map = [list(line) for line in str_input.split("\n")]
    loop = find_loop(pipe_map)
    outside_loop = []
    for i,pipe in enumerate(loop[1:] + [loop[0]], start = 1):
        if pipe[0] > loop[i-1][0]:
            step = [0,-1]
        elif pipe[0] < loop[i-1][0]:
            step = [0,1]
        elif pipe[1] > loop[i-1][1]:
            step = [1,0]
        else:
            step = [-1,0]
        find_all_to_left(pipe_map, loop, outside_loop, pipe, step)
        
        symbol = pipe_map[pipe[1]][pipe[0]]
        if symbol in CORNERS.keys():
            print(symbol, step)
            find_all_to_left(pipe_map, loop, outside_loop, pipe, corner_vectors[symbol][str(step)])

    print(len(pipe_map[0])*len(pipe_map) - len(loop), len(outside_loop))
    return len(outside_loop)


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