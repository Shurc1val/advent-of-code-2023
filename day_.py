import pytest

from read_data_function import read_data

# ----- PART ONE -----


def part_one(str_input: str):
    pass


def test_part_one():
    assert part_one("""""") == None


# ----- PART TWO -----


def part_two(str_input: str):
    pass


def test_part_two():
    assert part_two("""""") == None


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_.txt")))
    print(part_two(read_data("day_.txt")))