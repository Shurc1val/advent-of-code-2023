import pytest

from read_data_function import read_data

# ----- PART ONE -----


def display_grid(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))


def roll_north(grid: list[list[int]]):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'O':
                count = 0
                while (i - count > 0) and grid[i - count - 1][j] not in ['O', '#']:
                    grid[i - count - 1][j] = "O"
                    grid[i - count][j] = "."
                    count += 1


def get_load(grid: list[list[str]]):
    load = 0
    for i, row in enumerate(grid):
        for j, space in enumerate(row):
            if space == 'O':
                load += len(grid) - i
    return load


def part_one(str_input: str):
    grid = [list(row) for row in str_input.split('\n')]
    roll_north(grid)
    return get_load(grid)


def test_part_one():
    assert part_one("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""") == 136


# ----- PART TWO -----


def grid_to_string(grid: list[list[str]]) -> str:
    return '\n'.join([''.join(row) for row in grid])


def string_to_grid(grid_string: str) -> list[list[str]]:
    return [list(row) for row in grid_string.split('\n')]


def cycle(grid: list[list[int]]):
    num_tilts = 0
    while num_tilts < 4:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 'O':
                    count = 0
                    while (i - count > 0) and grid[i - count - 1][j] not in ['O', '#']:
                        grid[i - count - 1][j] = "O"
                        grid[i - count][j] = "."
                        count += 1

        num_tilts += 1

        # Rotate grid clockwise:
        grid = [list(row) for row in list(zip(*grid[::-1]))]

    return grid


def part_two(str_input: str, n: int):
    grid = [list(row) for row in str_input.split('\n')]
    grid_memory = []
    for i in range(n):
        str_grid = grid_to_string(grid)
        if str_grid in grid_memory:
            grid_memory = grid_memory[grid_memory.index(str_grid):]
            grid = string_to_grid(grid_memory[(n - i)%len(grid_memory)])
            break
        grid_memory.append(str_grid)
        grid = cycle(grid)
    return get_load(grid)


def test_part_two():
    assert part_two("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""", 1000000000) == 64


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_14.txt")))
    print(part_two(read_data("day_14.txt"), 1000000000))