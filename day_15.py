import pytest

from read_data_function import read_data

# ----- PART ONE -----


def hash_function(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value = value % 256
    return value


def part_one(str_input: str):
    strings = str_input.replace('\n','').split(',')
    return sum([hash_function(string) for string in strings])


def test_part_one():
    assert hash_function("HASH") == 52
    assert part_one("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7") == 1320


# ----- PART TWO -----

def hashmap(string: str, boxes: dict):
    if '-' in string:
        label = string[:-1]

        box_num = hash_function(label)
        box = boxes.get(box_num)

        if (box is not None) and (box.get(label) is not None):
            box.pop(label)

    else:
        label, focal_length = string.split('=')
        focal_length = int(focal_length)

        box_num = hash_function(label)
        box = boxes.get(box_num, None)

        if box is None:
            boxes[box_num] = {
                    label: focal_length
                }
        else:
            boxes[box_num][label] = focal_length



def focusing_power(boxes: dict) -> int:
    total_power = 0
    for box_num in boxes:
        for j, focal_length in enumerate(boxes[box_num].values(), start=1):
            total_power += (box_num + 1) * j * focal_length
    return total_power


def part_two(str_input: str):
    strings = str_input.replace('\n','').split(',')
    boxes = {}
    for string in strings:
        hashmap(string, boxes)

    return focusing_power(boxes)


def test_part_two():
    assert part_two("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""") == 145


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_15.txt")))
    print(part_two(read_data("day_15.txt")))