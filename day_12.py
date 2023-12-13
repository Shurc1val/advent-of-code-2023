from copy import deepcopy
from itertools import product
import pytest

from read_data_function import read_data

# ----- PART ONE -----


def check_row_valid(row: str, experiment_row: str):
    if len(row) != len(experiment_row):
        return False
    
    for i in range(len(row)):
        if (row[i] != '?') and (row[i] != experiment_row[i]):
            return False
    return True


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


def get_number_substring_arrangements(string_length: int, substring_lengths: list[int], cache_dict: dict = None):
    """NOTE - substring lengths are ordered"""
    if cache_dict is None:
        cache_dict = {}
    if sum(substring_lengths) > string_length:
        return 0
    
    if (sum(substring_lengths) == string_length) or (substring_lengths == []):
        return 1
    
    num_arrangements = 0
    for i in range(0, string_length - substring_lengths[0] + 1):
        num = cache_dict.get(f'{i} {str(substring_lengths[1:])}', None)
        if num is None:
            num = get_number_substring_arrangements(i, substring_lengths[1:], cache_dict)
            cache_dict[f'{i} {str(substring_lengths[1:])}'] = num
        num_arrangements += num
    
    return num_arrangements


def possible_no_hash_options(row: int, numbers_alt: list[int], cache_dict: dict = None):
    if cache_dict is None:
        cache_dict = {}

    if sum(numbers_alt) > len(row):
        return 0
    
    if row.count('.') > 0:
        num_correct_combos = 0
        sub_row = len(row.split('.', 1)[0]) + 1
        for i in range(0, len(numbers_alt) + 1):
                if sum(numbers_alt[:i]) <= sub_row and sum(numbers_alt[i:]) <= len(row) - sub_row:
                    rem_row = row.split('.', 1)[1]
                    rem_nums = numbers_alt[i:]
                    rem_options = cache_dict.get(f'{str(rem_row)} {str(rem_nums)}', None)
                    if rem_options is None:
                        rem_options = possible_no_hash_options(rem_row, rem_nums, cache_dict)
                        
                    num = get_number_substring_arrangements(sub_row, numbers_alt[:i])
                    num_correct_combos += num * rem_options
    else:
        num_correct_combos = get_number_substring_arrangements(len(row), numbers_alt)

    cache_dict[f'{str(row)} {str(numbers_alt)}'] = num_correct_combos
    return num_correct_combos


def get_num_combinations_for_row(row: str, numbers: list[int], cache_dict: dict = None) -> int:
    if cache_dict is None:
        cache_dict = {}

    if row == "???" and numbers == [1]:
        pass

    num_correct_combos = 0

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
                    
    else:
        num_correct_combos = cache_dict.get(f'{row} {numbers}')
        if num_correct_combos is None: 
            num_correct_combos = possible_no_hash_options(row, [number + 1 for number in numbers])
        
    cache_dict[f'{str(row)} {str(numbers)}'] = num_correct_combos
    return num_correct_combos


def part_one(str_input: str):
    lines = str_input.split('\n')
    spring_rows = [(line.split()[0] + '.') for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')] for line in lines]
    sum = 0
    for i, inputs in enumerate(zip(spring_rows, spring_numbers)):
        num = get_num_combinations_for_row(inputs[0],inputs[1])
        sum += num
    return sum
    

def test_part_one():
    '''assert check_row_valid('??#?###', '#.#.###') == True
    assert check_row_valid('??#?###', '#...###') == False
    assert part_one('???.### 1,1,3') == 1
    assert part_one('?###???????? 3,2,1') == 10
    assert possible_no_hash_options('??...', [2]) == 2
    assert possible_no_hash_options('??...', [2,2]) == 0
    assert possible_no_hash_options('.??..??...', [2,2]) == 4
    assert possible_no_hash_options('???', [1]) == 3
    assert part_one('.??..??...?##. 1,1,3') == 4
    assert part_one('?#?#?#?#?#?#?#? 1,3,1,6') == 1
    assert part_one('?.???.???? 1,1,1') == 29
    assert part_one("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 21
    assert part_one('?#?#?#?#?#?#?#? 1,3,1,6') == 1'''
    assert get_num_combinations_for_row('???', [1]) == 2
    assert part_one('?????.?#.???#?#??? 2,1,2,1,4,1') == 12
    assert part_one('.????.??#?#? 1,5') == 8


# ----- PART TWO -----

from datetime import datetime


def part_two(str_input: str):
    lines = str_input.split('\n')
    spring_rows = [('?'.join(5*[line.split()[0]]) + '.') for line in lines]
    spring_numbers = [[int(num) for num in line.split()[1].split(',')]*5 for line in lines]
    sum = 0
    for i, inputs in enumerate(zip(spring_rows, spring_numbers)):
        print(i, lines[i])
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
    assert part_two("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""") == 3*525152
    assert get_number_substring_arrangements(4, [2]) == 3
    assert get_number_substring_arrangements(4, [1,1]) == 6
    assert get_number_substring_arrangements(6, [2,1,1]) == 10
    assert get_number_substring_arrangements(6, [1,1,1]) == 20
    assert possible_no_hash_options('?.???.????.', [2,2,2]) == 29


# --------------------


if __name__ == "__main__":
    part_one('?????.?#.???#?#??? 2,1,2,1,4,1')
    print(part_one(read_data("day_12.txt")))
    print(part_two(read_data("day_12.txt")))