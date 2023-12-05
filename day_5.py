import pytest
from copy import deepcopy

from read_data_function import read_data


# ----- PART ONE -----


def source_to_destination(source_numbers: list[int], map_lines: list[str]) -> int:
    for i, source_number in enumerate(source_numbers):
        j = 0
        bln_marker = False
        while not bln_marker and j < len(map_lines):
            map_line = [int(num) for num in map_lines[j].split()]
            if source_number in range(map_line[1], map_line[1] + map_line[2]):
                source_numbers[i] = map_line[0] + (source_number - map_line[1])
                bln_marker = True
            j += 1



def part_one(str_input: str):
    seeds = [int(num) for num in str_input.split('\n\n')[0].lstrip('seeds: ').split()]
    maps = [lines.split(":")[1].strip() for lines in str_input.split("\n\n")[1:]]
    for map in maps:
        source_to_destination(seeds, map.split('\n'))
    return min(seeds)

def test_part_one():
    seeds = [79, 14, 55, 13]
    source_to_destination(seeds, ["50 98 2", "52 50 48"])
    assert seeds == [81, 14, 57, 13]
    assert part_one("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""") == 35


# ----- PART TWO -----


def source_to_destination_2(source_numbers: list[int], map_lines: list[str]) -> int:
    i = 0
    while i < len(source_numbers):
        number_range = deepcopy(source_numbers[i])
        j = 0
        bln_marker = False
        while not bln_marker and j < len(map_lines):
            map_line = [int(num) for num in map_lines[j].split()]
            map_line_range = [map_line[1], map_line[1] + map_line[2] - 1]
            
            if (number_range[0] >= map_line_range[0]) and (number_range[1] <= map_line_range[1]):
                source_numbers[i][0] = map_line[0] + (number_range[0]- map_line[1])
                source_numbers[i][1] = map_line[0] + (number_range[1]- map_line[1])
                bln_marker = True
            elif (number_range[0] >= map_line_range[0]) and (number_range[0] <= map_line_range[1]):
                source_numbers[i][0] = map_line[0] + (number_range[0]- map_line[1])
                source_numbers[i][1] = map_line[0] + map_line[2]
                source_numbers.append(
                    [map_line_range[1] + 1, number_range[1]]
                )
                bln_marker = True
            elif (number_range[1] <= map_line_range[1]) and (number_range[1] >= map_line_range[0]):
                source_numbers[i][1] = map_line[0] + (number_range[1]- map_line[1])
                source_numbers[i][0] = map_line[0]
                source_numbers.append(
                    [number_range[0], map_line_range[0] - 1]
                )
                bln_marker = True
            elif ((number_range[0] < map_line_range[0]) and (number_range[1] > map_line_range[-1])):
                source_numbers[i][0] = map_line[0]
                source_numbers[i][1] = map_line[0] + map_line[2]
                source_numbers.append(
                    [number_range[0], map_line_range[0] - 1]
                )
                source_numbers.append(
                    [map_line_range[-1] + 1, number_range[1]]
                )
            j += 1
        i += 1 


def part_two(str_input: str):
    seed_range_nums = [int(num) for num in str_input.split('\n\n')[0].lstrip('seeds: ').split()]
    seeds = []
    for i in range(0, len(seed_range_nums), 2):
        seeds.append([seed_range_nums[i], seed_range_nums[i] + seed_range_nums[i+1] - 1])
    maps = [lines.split(":")[1].strip() for lines in str_input.split("\n\n")[1:]]
    for map in maps:
        source_to_destination_2(seeds, map.split('\n'))
    return min([seed_range[0] for seed_range in seeds])


def test_part_two():
    assert part_two("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""") == 46


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_5.txt")))
    print(part_two(read_data("day_5.txt")))