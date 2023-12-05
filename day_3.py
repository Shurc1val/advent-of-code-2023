import pytest

from read_data_function import read_data

# ----- PART ONE -----


def find_number_range(line: str, first_index: int):
    count = first_index
    while count < len(line) and line[count].isdigit():
        count += 1
    return count


def check_symbol_adjacency(lines: list[str], indices: list[int]) -> bool:
    for i in range(max(indices[0]-1, 0), min(indices[0]+2, len(lines))):
        for j in range(max(indices[1]-1, 0), min(indices[1]+2, len(lines[0]))):
            if (not lines[i][j].isdigit()) and (lines[i][j] != '.'):
                return True
    return False


def part_one(str_input: str):
    part_sum = 0
    
    lines = str_input.split("\n")
    for i,line in enumerate(lines):
        j = 0
        while j < len(line):
            if line[j].isdigit():
                end = find_number_range(line, j)
                if any([check_symbol_adjacency(lines, [i,k]) for k in range(j,end)]):
                    part_sum += int(lines[i][j:end])
                j = end
            else:
                j += 1
    return part_sum

def test_part_one():
    assert part_one("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""") == 4361


# ----- PART TWO -----

def find_adjacent_asterisks(lines: list[str], indices: list[int], number_considered: int, asterisk_dict: list):
    for i in range(max(indices[0]-1, 0), min(indices[0]+2, len(lines))):
        for j in range(max(indices[1]-1, 0), min(indices[1]+2, len(lines[0]))):
            if lines[i][j] == '*':
                if not asterisk_dict.get(str([i,j]), None):
                    asterisk_dict[str([i,j])] = []
                asterisk_dict[str([i,j])].append(number_considered)
                return True
    return False


def part_two(str_input: str):
    part_sum = 0
    asterisk_dict = {}
    lines = str_input.split("\n")
    for i,line in enumerate(lines):
        j = 0
        while j < len(line):
            if line[j].isdigit():
                end = find_number_range(line, j)
                k = j
                while k < end:
                    if find_adjacent_asterisks(lines, [i,k], int(lines[i][j:end]), asterisk_dict):
                        k = end
                    else:
                        k += 1
                j = end
            else:
                j += 1
    return sum([asterisk[0] * asterisk[1] for asterisk in asterisk_dict.values() if len(asterisk) == 2])


def test_part_two():
    assert part_two("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""") == 467835


# --------------------


if __name__ == "__main__":

    print(part_one(read_data("day_3.txt")))
    print(part_two(read_data("day_3.txt")))