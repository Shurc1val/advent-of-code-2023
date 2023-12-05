import pytest

from read_data_function import read_data

# ----- PART ONE -----


def min_colour_nums_for_game(str_hands: str) -> dict:
    game_number = int(str_hands.split(":")[0].lstrip("Game "))
    game = {
        "game_number": game_number,
        "red": 0,
        "green": 0,
        "blue": 0
    }
    hands = [hand.split(",") for hand in str_hands.split(":")[1].split(";")]
    for hand in hands:
        for set in hand:
            colour = set.strip().split(" ")[1]
            number = int(set.strip().split(" ")[0])
            if number > game[colour]:
                game[colour] = number

    return game


def game_possible(game: dict) -> bool:
    bag = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for colour in bag:
        if game[colour] > bag[colour]:
            return False
    return True


def sum_of_possible_game_ids(str_input: str):
    games = [min_colour_nums_for_game(str_game) for str_game in str_input.split("\n")]
    return sum([game['game_number'] for game in games if game_possible(game)])
    pass


def test_part_one():
    assert sum_of_possible_game_ids("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""") == 8


# ----- PART TWO -----


def sum_of_game_powers(str_input: str):
    games = [min_colour_nums_for_game(str_game) for str_game in str_input.split("\n")]
    return sum([game['red']*game['green']*game['blue'] for game in games])


def test_part_two():
    assert sum_of_game_powers("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""") == 2286


# --------------------


if __name__ == "__main__":
    print(sum_of_possible_game_ids(read_data("day_2.txt")))
    print(sum_of_game_powers(read_data("day_2.txt")))