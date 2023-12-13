import pytest

from read_data_function import read_data

# ----- PART ONE -----

def display_grid(grid: list[list[str]]):
    for row in grid:
        print(''.join(row))


def find_reflection_num(grid: list[list[str]]) -> int:
    reflection_lines = []

    for i in range(len(grid) - 1):
        bln_perfect = True
        count = 0
        while ((i-count) >= 0) and ((i+1+count) < len(grid)):
            if grid[i-count] != grid[i+1+count]:
                bln_perfect = False
                break
            count += 1
        if bln_perfect:
            reflection_lines.append({
                'num': 100*(i+1),
                'reflected': count
                })
        
    for i in range(len(grid[0]) - 1):
        bln_perfect = True
        count = 0
        while ((i-count) >= 0) and ((i+1+count) < len(grid[0])):
            if any([row[i-count] != row[i+1+count] for row in grid]):
                bln_perfect = False
                break
            count += 1
        if bln_perfect:
            reflection_lines.append({
                'num': i + 1,
                'reflected': count
                })
                
    #reflection_lines.sort(key = lambda x: x['reflected'])
    return reflection_lines[-1]['num']


def part_one(str_input: str):
    string_grids = str_input.split('\n\n')
    grids = [[list(row) for row in string_grid.split('\n')] for string_grid in string_grids]
    '''for grid in grids:
        display_grid(grid)
        print(find_reflection_num(grid))'''
    return sum([find_reflection_num(grid) for grid in grids])


def test_part_one():
    assert part_one("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""") == 5
    assert part_one("""#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""") == 400    
    assert part_one("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""") == 405


# ----- PART TWO -----

SYMBOL_OPPOSITES = {
    '.': '#',
    '#': '.'
}


def line_difference(line_1: list[str], line_2: list[str]) -> list[int]:
    differences = []
    for i in range(len(line_1)):
        if line_1[i] != line_2[i]:
            differences.append(i)
    return differences


def smudge_detector(grid: list[list[str]]) -> int:
    reflection_lines = []

    for i in range(len(grid) - 1):
        bln_perfect = True
        run_counter = 0
        count = 0
        index = -1
        while bln_perfect and run_counter < 2:
            while ((i-count) >= 0) and ((i+1+count) < len(grid)):
                if grid[i-count] != grid[i+1+count]:
                    bln_perfect = False
                    break
                count += 1
            if (not bln_perfect) and run_counter == 0:
                differences = line_difference(grid[i-count], grid[i+1+count])
                if len(differences) == 1:
                    index = i-count
                    grid[index][differences[0]] = SYMBOL_OPPOSITES[grid[index][differences[0]]]
                    bln_perfect = True
            elif bln_perfect and run_counter == 1:
                return 100*(i+1)
            else:
                bln_perfect = False
            run_counter += 1
        if index >= 0:
            grid[index][differences[0]] = SYMBOL_OPPOSITES[grid[index][differences[0]]]

    grid_flipped = [[row[i] for row in grid] for i in range(len(grid[0]))]

    for i in range(len(grid_flipped) - 1):
        bln_perfect = True
        run_counter = 0
        count = 0
        index = -1
        while bln_perfect and run_counter < 2:
            while ((i-count) >= 0) and ((i+1+count) < len(grid_flipped)):
                if grid_flipped[i-count] != grid_flipped[i+1+count]:
                    bln_perfect = False
                    break
                count += 1
            if (not bln_perfect) and run_counter == 0:
                differences = line_difference(grid_flipped[i-count], grid_flipped[i+1+count])
                if len(differences) == 1:
                    index = i-count
                    grid_flipped[index][differences[0]] = SYMBOL_OPPOSITES[grid_flipped[index][differences[0]]]
                    bln_perfect = True
            elif bln_perfect and run_counter == 1:
                return i+1
            else:
                bln_perfect = False
            run_counter += 1
        if index >= 0:
            grid_flipped[index][differences[0]] = SYMBOL_OPPOSITES[grid_flipped[index][differences[0]]]



def part_two(str_input: str):
    string_grids = str_input.split('\n\n')
    grids = [[list(row) for row in string_grid.split('\n')] for string_grid in string_grids]
    return sum([smudge_detector(grid) for grid in grids])


def test_part_two():
    assert part_two("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""") == 300
    assert part_two("""#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""") == 100
    assert part_two("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""") == 400


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_13.txt")))
    print(part_two(read_data("day_13.txt")))