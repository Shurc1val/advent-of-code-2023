import pytest

from read_data_function import read_data

# ----- PART ONE -----


def expand_universe(universe: list[list[str]]):
    rows_to_repeat = []
    for i, row in enumerate(universe):
        if all([place == '.' for place in row]):
            rows_to_repeat.append(i)
    for i, index in enumerate(rows_to_repeat):
        adj_index = index + i
        universe = universe[:adj_index + 1] + universe[adj_index:]

    columns_to_repeat = []
    for i, column in enumerate([[row[i] for row in universe] for i in range(len(universe[0]))]):
        if all([place == '.' for place in column]):
            columns_to_repeat.append(i)
    for i, index in enumerate(columns_to_repeat):
        adj_index = index + i
        for i in range(len(universe)):
            universe[i] = universe[i][:adj_index + 1] + universe[i][adj_index:]

    return universe
    

def find_galaxies(universe: list[list[str]]) -> list[list[int]]:
    galaxies = []
    for i,row in enumerate(universe):
        for j,place in enumerate(row):
            if place == '#':
                galaxies.append([j,i])

    return galaxies


def get_distance(galaxy_1: list[int], galaxy_2: list[int]) -> int:
    return abs(galaxy_2[0] - galaxy_1[0]) + abs(galaxy_2[1] - galaxy_1[1])


def part_one(str_input: str):
    universe = [list(row) for row in str_input.split('\n')]
    universe = expand_universe(universe)
    galaxies = find_galaxies(universe)
    shortest_path = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            shortest_path += get_distance(galaxies[i], galaxies[j])
            
    
    return shortest_path


def test_part_one():
    assert expand_universe([list(row) for row in """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".split('\n')]) == [list(row) for row in """....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......""".split('\n')]
    assert get_distance([1,6], [5,11]) == 9
    assert part_one("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""") == 374


# ----- PART TWO -----



def get_repeated_rows_and_columns(universe: list[list[str]]):
    rows_to_repeat = []
    for i, row in enumerate(universe):
        if all([place == '.' for place in row]):
            rows_to_repeat.append(i)

    columns_to_repeat = []
    for i, column in enumerate([[row[i] for row in universe] for i in range(len(universe[0]))]):
        if all([place == '.' for place in column]):
            columns_to_repeat.append(i)

    return rows_to_repeat, columns_to_repeat
    

def find_galaxies(universe: list[list[str]]) -> list[list[int]]:
    galaxies = []
    for i,row in enumerate(universe):
        for j,place in enumerate(row):
            if place == '#':
                galaxies.append([j,i])

    return galaxies


def get_distance_v2(galaxy_1: list[int], galaxy_2: list[int], repeat_rows: list[int], repeat_columns: list[int], repeat_factor: int) -> int:
    distance = abs(galaxy_2[0] - galaxy_1[0]) + abs(galaxy_2[1] - galaxy_1[1])
    for row in repeat_rows:
        if row in list(range(min(galaxy_1[1], galaxy_2[1]), max(galaxy_1[1], galaxy_2[1]) + 1)):
            distance += repeat_factor - 1
    
    for column in repeat_columns:
        if column in list(range(min(galaxy_1[0], galaxy_2[0]), max(galaxy_1[0], galaxy_2[0]) + 1)):
            distance += repeat_factor - 1

    return distance


def part_two(str_input: str, repeat_factor: int):
    universe = [list(row) for row in str_input.split('\n')]
    repeat_rows, repeat_columns = get_repeated_rows_and_columns(universe)
    galaxies = find_galaxies(universe)
    shortest_path = 0
    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            shortest_path += get_distance_v2(galaxies[i], galaxies[j], repeat_rows, repeat_columns, repeat_factor)
            
    return shortest_path


def test_part_two():
    assert part_two("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 2) == 374
    assert part_two("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 10) == 1030
    assert part_two("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", 100) == 8410


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_11.txt")))
    print(part_two(read_data("day_11.txt"), 1000000))