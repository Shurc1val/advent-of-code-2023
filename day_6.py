"""
We want to maximise, with respect to x
F(t,x) = (t-x)*x
or rather
f(x) = (T-x)x = Tx - x**2,
considering T as a fixed constant; this is a negative quadratic that will have one turning point at
f'(x) = 0 = T - 2x
=> x = T/2 is the max charge time for any T.

if f(x) = k, => f - k = 0 = x**2 - Tx + k
=> x = (T +- (T**2 - 4k)^(1/2))2
"""

import pytest
import math

from read_data_function import read_data

# ----- PART ONE -----


def distance_in_race(time: int, charge_time: int) -> int:
    return (time - charge_time) * charge_time


def get_num_winning_options(time: int, record: int) -> int:
    count = 0
    for i in range(1, time):
        if distance_in_race(time, i) > record:
            count += 1
    return count


def part_one(str_input: str) -> int:
    times = [int(num) for num in str_input.split('\n')[0].split(':')[1].strip().split()]
    records = [int(num) for num in str_input.split('\n')[1].split(':')[1].strip().split()]
    product = 1
    for race in zip(times, records):
        product *= get_num_winning_options(race[0], race[1])
    return product


def test_part_one():
    assert get_num_winning_options(7, 9) == 4
    assert get_num_winning_options(15, 40) == 8
    assert part_one("""Time:      7  15   30
Distance:  9  40  200""") == 288


# ----- PART TWO -----

def get_record_charge_times(time: int, record: int) -> list[int]:
    return [(time + math.sqrt(time**2 - 4*record))/2, (time - math.sqrt(time**2 - 4*record))/2]


def part_two(str_input: str):
    time = int(str_input.split('\n')[0].split(':')[1].strip().replace(" ", ""))
    record = int(str_input.split('\n')[1].split(':')[1].strip().replace(" ", ""))
    record_charge_times = get_record_charge_times(time, record)
    return math.floor(record_charge_times[0] - record_charge_times[1])


def test_part_two():
    assert part_two("""Time:      7  15   30
Distance:  9  40  200""") == 71503


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_6.txt")))
    print(part_two(read_data("day_6.txt")))