from copy import deepcopy
from itertools import product
import pytest

from read_data_function import read_data

# ----- PART ONE -----


def check_row_valid(row: str, experiment_row: str):
    for i in range(len(row)):
        if (row[i] != '?') and (row[i] != experiment_row[i]):
            return False
    return True


def check_partial_combination(row: str, spring_strings: list[str], combination: list[int]):
    experiment_row = ''.join([combination[i] + spring_strings[i] for i in range(len(combination))])
    exp_row_length = len(experiment_row)
    if not check_row_valid(row[:exp_row_length], experiment_row):
        return False
    remaining_row_hashes = row[exp_row_length:].count('#')
    spring_lengths = [len(spring_string) - 1 for spring_string in spring_strings]
    if (experiment_row.count('#') + remaining_row_hashes) > (sum(spring_lengths) + 1):
        return False
    if (remaining_row_hashes + row[exp_row_length:].count('?')) < (sum(spring_lengths[len(combination):]) + 1):
        return False
    return True


def get_possible_space_combinations_validate(sum_value: int, num_spaces: int, row: str, spring_strings: list[str], prefix: list[int] = None):
    if prefix is None:
        prefix = []

    if num_spaces == 1:
        prefix.append(sum_value*'.')
        return [prefix]
    
    if prefix and not check_partial_combination(row, spring_strings, prefix):
        return []

    options = []
    for i in range(sum_value + 1):
        options += get_possible_space_combinations_validate(sum_value - i, num_spaces - 1, row, spring_strings, prefix + [i*'.'])
    return options


def get_num_combinations_for_row(row: str, numbers: list[int]) -> int:
    spring_strings = [f"{'#'*number}." for number in numbers]
    spring_strings[-1] = spring_strings[-1].rstrip('.')
    num_spaces_to_fill = len(row) - len(''.join(spring_strings))
    print(row, numbers, num_spaces_to_fill)
    possible_space_combinations = get_possible_space_combinations_validate(num_spaces_to_fill, len(spring_strings) + 1, row, spring_strings)
    num_correct_combos = 0
    for combination in possible_space_combinations:
        experiment_row = ''.join(list(map(lambda x: x[0] + x[1], zip(combination, spring_strings)))) + combination[-1]
        if check_row_valid(row, experiment_row):
            num_correct_combos += 1
    return num_correct_combos


def part_one(str_input: str):
    lines = str_input.split('\n')
    spring_rows = [line.split()[0] for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')] for line in lines]
    return sum(get_num_combinations_for_row(inputs[0],inputs[1]) for inputs in zip(spring_rows, spring_numbers))
    


def test_part_one():
    assert check_row_valid('??#?###', '#.#.###') == True
    assert check_row_valid('??#?###', '#...###') == False
    assert get_num_combinations_for_row('???.###', [1,1,3]) == 1
    assert get_num_combinations_for_row('?###????????', [3,2,1]) == 10
    assert part_one("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 21


# ----- PART TWO -----


def part_two(str_input: str):
    lines = str_input.split('\n')
    print(len(lines))
    spring_rows = [((line.split()[0] + '?')*5)[:-1] for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')]*5 for line in lines]
    sum = 0
    for i, inputs in enumerate(zip(spring_rows, spring_numbers)):
        num_comb = get_num_combinations_for_row(inputs[0],inputs[1])
        print(i, num_comb)
        sum += num_comb
    return sum


def test_part_two():
    assert part_two("""???.### 1,1,3""") == 1
    assert part_two(".??..??...?##. 1,1,3") == 16384
    assert part_two("?###???????? 3,2,1") == 506250
    assert part_two("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 525152


# --------------------


if __name__ == "__main__":
    print(part_two(read_data("day_12.txt")))