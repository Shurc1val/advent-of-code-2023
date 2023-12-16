from copy import deepcopy
import pytest
import os

from read_data_function import read_data

# ----- PART ONE -----

# (y, x), with y increasing downwards

REFLECTION_DICT = {
    '-': {
        '[0, 1]': [0, 1],
        '[0, -1]': [0, -1],
        '[1, 0]': [
            [0, -1],
            [0, 1]
            ],
        '[-1, 0]': [
            [0, -1],
            [0, 1]
            ]
    },
    '|': {
        '[0, 1]': [
            [1, 0],
            [-1, 0]
            ],
        '[0, -1]': [
            [1, 0],
            [-1, 0]
            ],
        '[1, 0]': [1, 0],
        '[-1, 0]': [-1, 0]
    },
    '/': {
        '[0, 1]': [-1, 0],
        '[0, -1]': [1, 0],
        '[1, 0]': [0, -1],
        '[-1, 0]': [0, 1] 
    },
    '{': {
        '[0, 1]': [1, 0],
        '[0, -1]': [-1, 0],
        '[1, 0]': [0, 1],
        '[-1, 0]': [0, -1]
    }
}


def read_raw_data(filename: str) -> str:
    """Function to return the whole of the string contents of a file as a raw string."""
    with open(os.path.join("puzzle_inputs", filename), 'r') as file:
        data = file.read().replace('\n', 'newline').replace('\\', '{').lstrip('\'').rstrip('\'')
    return data


def format_grid(str_input: str) -> list[list[str]]:
    str_input = str_input.replace('\n', 'newline').replace('\\', '{').lstrip('\'').rstrip('\'')
    return [list(line) for line in str_input.split('newline')]


def light_traverser(mirror_grid: list[list[str]], energy_grid: list[list[int]], current: list[int], change: list[int]):
    current = list(map(lambda a,b: a + b, current, change))

    while ((0 <= current[0]) and (current[0] < len(mirror_grid)) and \
           (0 <= current[1]) and (current[1] < len(mirror_grid[0]))) and \
            (energy_grid[current[0]][current[1]] != change):

        mirror = mirror_grid[current[0]][current[1]]
        energy_grid[current[0]][current[1]] = change

        if mirror != '.':
            change = REFLECTION_DICT[mirror][str(change)]

        if isinstance(change[0], list):
            light_traverser(mirror_grid, energy_grid, current, change[-1])
            change = change[0]

        current = list(map(lambda a,b: a + b, current, change))


def part_one(str_input: str):
    mirror_grid = format_grid(str_input)
    energy_grid = [[None for i in range(len(mirror_grid[0]))] for j in range(len(mirror_grid))]
    light_traverser(mirror_grid, energy_grid, [0,-1], [0,1])
    energy = 0
    for row in energy_grid:
        energy += sum([1 for cell in row if cell])

    return energy


def test_part_one():
    assert part_one(r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""") == 46


# ----- PART TWO -----

def get_possible_starts(mirror_grid: list[list[str]]) -> list[dict]:
    possible_starts = []
    for i in range(len(mirror_grid)):
        possible_starts.append({
            'start': [i, -1],
            'change': [0, 1]
        })
        possible_starts.append({
            'start': [i, len(mirror_grid[0])],
            'change': [0, -1]
        })

    for i in range(len(mirror_grid[0])):
        possible_starts.append({
            'start': [-1, i],
            'change': [1, 0]
        })
        possible_starts.append({
            'start': [len(mirror_grid), i],
            'change': [-1, 0]
        })

    return possible_starts


def part_two(str_input: str):
    mirror_grid = format_grid(str_input)
    energies = []
    possible_starts = get_possible_starts(mirror_grid)
    for possible_start in possible_starts:
        energy_grid = [[None for i in range(len(mirror_grid[0]))] for j in range(len(mirror_grid))]
        light_traverser(mirror_grid, energy_grid, possible_start['start'], possible_start['change'])
        energy = 0
        for row in energy_grid:
            energy += sum([1 for cell in row if cell])
        energies.append(energy)

    return max(energies)


def test_part_two():
    assert part_two(r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""") == 51


# --------------------


if __name__ == "__main__":
    print(part_one(read_raw_data("day_16.txt")))
    print(part_two(read_raw_data("day_16.txt")))