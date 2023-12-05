import pytest
from read_data_function import read_data

# ----- PART ONE -----


def get_number_from_string(line: str) -> int:
    digits = [char for char in line if char.isdigit()]
    return int(digits[0] + digits[-1])


def sum_of_calibration_numbers(str_input: str) -> int:
    return sum([get_number_from_string(line) for line in str_input.split("\n")])


@pytest.mark.parametrize('line, number', [
    ("1abc2", 12),
    ("pqr3stu8vwx", 38),
    ("a1b2c3d4e5f", 15),
    ("treb7uchet", 77)
])
def test_get_number_from_string(line: str, number: int):
    assert get_number_from_string(line) == number


def test_sum_of_calibration_numbers():
    assert sum_of_calibration_numbers("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""") == 142


# ----- PART TWO -----


NUMBER_WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"}


def get_number_from_string_2(line: str) -> int:
    digits = []
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(line[i])
        for j in range(i+2, len(line) + 1):
            if line[i:j] in NUMBER_WORDS:
                digits.append(NUMBER_WORDS[line[i:j]])
    return int(digits[0] + digits[-1])


def sum_of_calibration_numbers_2(str_input: str) -> int:
    return sum([get_number_from_string_2(line) for line in str_input.split("\n")])


@pytest.mark.parametrize('line, number', [
    ("two1nine", 29),
    ("eightwothree", 83),
    ("abcone2threexyz", 13),
    ("xtwone3four", 24),
    ("4nineeightseven2", 42),
    ("zoneight234", 14),
    ("7pqrstsixteen", 76)
])
def test_get_number_from_string_2(line: str, number: int):
    assert get_number_from_string_2(line) == number


def test_sum_of_calibration_numbers_2():
    assert sum_of_calibration_numbers_2("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""") == 281


if __name__ == "__main__":
    print(sum_of_calibration_numbers_2(read_data("day_1.txt")))