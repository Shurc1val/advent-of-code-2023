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
    
    if len(row[exp_row_length:]) < sum([len(spring_string) for spring_string in spring_strings[len(combination):]]):
        return False

    if row[exp_row_length:].count('?') + row[exp_row_length:].count('#') < sum([len(spring_string) - 1 for spring_string in spring_strings[len(combination):]]):
        return False
    
    if row[exp_row_length:].count('?') + row[exp_row_length:].count('.') < len(spring_strings) - len(combination):
        return False
    
    return True


def get_possible_space_combinations_validate(sum_value: int, num_spaces: int, row: str, spring_strings: list[str], prefix: list[int] = None):
    
    if prefix is None:
        if len(row) < sum([len(spring_string) for spring_string in spring_strings]):
            return []
        prefix = []

    if num_spaces == 1:
        prefix.append(sum_value*'.')
        return [prefix]
    
    if not check_partial_combination(row, spring_strings, prefix):
        return []

    options = []
    for i in range(sum_value + 1):
        options += get_possible_space_combinations_validate(sum_value - i, num_spaces - 1, row, spring_strings, prefix + [i*'.'])
    return options


def get_first_row_spring_string(row: str) -> list[dict]:
    for i, string in enumerate(row):
        if string == "#":
            count = 0
            while (i + count < len(row) - 1) and (row[i+count] == '#'):
                count += 1
            return {
                'start': i,
                'length': count
            }
    return None


def get_num_combinations_for_row(row: str, numbers: list[int], cache_dict: dict = None) -> int:
    if cache_dict is None:
        cache_dict = {}

    num_correct_combos = 0
    if numbers == [] and row.count('#') == 0:
        return 1
    if row == '':
        return 0

    first_row_spring_string = get_first_row_spring_string(row)
    spring_strings = [f"{'#'*number}." for number in numbers]
    if first_row_spring_string:
        for i, number in enumerate(numbers):
            for j in range(max(0, number - first_row_spring_string['length']) + 1):
                if check_row_valid(row[first_row_spring_string['start'] - j: first_row_spring_string['start'] - j + numbers[i] + 1], spring_strings[i]):
                    a_row = row[:first_row_spring_string['start'] - j]
                    a_nums = numbers[:i]
                    a = cache_dict.get(f'{str(a_row)} {str(a_nums)}', None)
                    if a is None:
                        a = get_num_combinations_for_row(a_row, a_nums, cache_dict)
                    b_row = row[first_row_spring_string['start'] - j + numbers[i] + 1:]
                    b_nums = numbers[i+1:]
                    b = cache_dict.get(f'{str(b_row)} {str(b_nums)}', None)
                    if b is None:
                        b = get_num_combinations_for_row(b_row, b_nums, cache_dict)
                    num_correct_combos += a * b
                    a_nums.clear(), b_nums.clear()
                    
    else:
        spring_strings = [f"{'#'*number}." for number in numbers]
        num_spaces_to_fill = len(row) - len(''.join(spring_strings))
        if num_spaces_to_fill and spring_strings:
            possible_space_combinations = get_possible_space_combinations_validate(num_spaces_to_fill, len(spring_strings) + 1, row, spring_strings)
            num_correct_combos = 0
            for combination in possible_space_combinations:
                experiment_row = ''.join(list(map(lambda x: x[0] + x[1], zip(combination, spring_strings)))) + combination[-1]
                if check_row_valid(row, experiment_row):
                    num_correct_combos += 1
        else:
            num_correct_combos = 1

    cache_dict[f'{str(row)} {str(numbers)}'] = num_correct_combos
    #print(row, numbers, num_correct_combos)
    return num_correct_combos


def part_one(str_input: str):
    lines = str_input.split('\n')
    spring_rows = [(line.split()[0] + '.') for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')] for line in lines]
    return sum(get_num_combinations_for_row(inputs[0],inputs[1]) for inputs in zip(spring_rows, spring_numbers))
    


def test_part_one():
    assert check_row_valid('??#?###', '#.#.###') == True
    assert check_row_valid('??#?###', '#...###') == False
    assert part_one('???.### 1,1,3') == 1
    assert part_one('?###???????? 3,2,1') == 10
    assert part_one('.??..??...?##. 1,1,3') == 4
    assert part_one('?#?#?#?#?#?#?#? 1,3,1,6') == 1
    assert part_one('?.???.???? 1,1,1') == 29
    assert part_one("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 21
    assert part_one('?#?#?#?#?#?#?#? 1,3,1,6') == 1


# ----- PART TWO -----

from datetime import datetime

def part_two(str_input: str):
    lines = str_input.split('\n')
    spring_rows = [((line.split()[0] + '?')*4 + line.split()[0] + '.') for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')]*5 for line in lines]
    sum = 0
    for i, inputs in enumerate(zip(spring_rows, spring_numbers)):
        if inputs[0].count('#') == 0:
            print(datetime.time(datetime.now()))
            print(i, inputs[0],inputs[1])
            sum += get_num_combinations_for_row(inputs[0],inputs[1])
            print(datetime.time(datetime.now()))
        else:
            print(i)
            sum += get_num_combinations_for_row(inputs[0],inputs[1])
    return sum


def test_part_two():
    assert part_two("""???.### 1,1,3""") == 1
    assert part_two(".??..??...?##. 1,1,3") == 16384
    assert part_two("?###???????? 3,2,1") == 506250
    assert part_two('?#?#?#?#?#?#?#? 1,3,1,6') == 1
    assert part_two("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 525152


# --------------------


if __name__ == "__main__":
    print(part_one('?.???.???? 1,1,1'))
    print(part_two('?.???.???? 1,1,1'))
    #print(part_two(read_data("day_12.txt")))