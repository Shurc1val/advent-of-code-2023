import pytest

from read_data_function import read_data

# ----- PART ONE -----

def get_differences(sequence: list[int]) -> list[int]:
    return [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]


def get_next_value(sequence: list[int]) -> int:
    differences = [sequence]
    while not all([num == 0 for num in differences[-1]]):
        differences.append(get_differences(differences[-1]))
    
    differences[-1].append(0)
    for i in range(-2, -(len(differences) + 1), -1):
        differences[i].append(differences[i][-1] + differences[i+1][-1])

    return differences[0][-1]


def part_one(str_input: str):
    sequences = [[int(num) for num in line.split()] for line in str_input.split('\n')]
    return sum([get_next_value(sequence) for sequence in sequences])


def test_part_one():
    assert get_next_value([0,3,6,9,12,15]) == 18
    assert get_next_value([1,3,6,10,15,21]) == 28
    assert get_next_value([10,13,16,21,30,45]) == 68
    assert part_one("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""") == 114


# ----- PART TWO -----


def get_previous_value(sequence: list[int]) -> int:
    return get_next_value(sequence[::-1])


def part_two(str_input: str):
    sequences = [[int(num) for num in line.split()] for line in str_input.split('\n')]
    return sum([get_previous_value(sequence) for sequence in sequences])


def test_part_two():
    assert get_previous_value([0,3,6,9,12,15]) == -3
    assert get_previous_value([1,3,6,10,15,21]) == 0
    assert get_previous_value([10,13,16,21,30,45]) == 5
    assert part_two("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""") == 2


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_9.txt")))
    print(part_two(read_data("day_9.txt")))