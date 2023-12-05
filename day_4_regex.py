import pytest
import re

from read_data_function import read_data

# ----- PART ONE -----


def get_card_points(card: str) -> int:
    winning_numbers = [int(num) for num in re.findall(r"(?:\s)*([0-9]+)", re.search(r"Card [0-9]+:\s((?:(?:\s)*[0-9]+)+)\s|", card).group())]
    print(winning_numbers)
    card_numbers = [int(num.strip()) for num in card.split(" | ")[1].split(" ") if num.isnumeric()]
    matches = len([num for num in card_numbers if num in winning_numbers])
    if matches:
        return 2**(matches - 1)
    return 0


def part_one(str_input: str):
    return sum([get_card_points(card) for card in str_input.split("\n")])


def test_part_one():
    assert part_one("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""") == 13


# ----- PART TWO -----


def get_new_cards_from_card(card: str, index: int, quantities: list[int]) -> int:
    winning_numbers = [int(num.strip()) for num in card.split(" | ")[0].split(" ") if num.isnumeric()]
    card_numbers = [int(num.strip()) for num in card.split(" | ")[1].split(" ") if num.isnumeric()]
    matches = len([num for num in card_numbers if num in winning_numbers])
    for i in range(index + 1, index + matches + 1):
        quantities[i] += quantities[index]


def part_two(str_input: str):
    cards = str_input.split("\n")
    quantities = [1] * len(cards)
    for i, card in enumerate(cards):
        get_new_cards_from_card(card, i, quantities)
    return sum(quantities)



def test_part_two():
    assert part_two("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""") == 30


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_4.txt")))
    print(part_two(read_data("day_4.txt")))