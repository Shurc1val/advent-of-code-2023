from itertools import product
import pytest

from read_data_function import read_data


# ----- PART ONE -----


def hand_score(hand: str) -> int:
    score = 0
    for char in hand:
        num_char = hand.count(char)
        remaining_cards = hand.replace(char, '')
        if num_char == 5 or num_char == 4:
            temp_score = num_char + 1
        elif num_char == 3:
            if remaining_cards.count(remaining_cards[0]) == 2:
                temp_score = 4
            else:
                temp_score = 3
        elif num_char == 2:
            if (remaining_cards.count(remaining_cards[0]) == 2) or (remaining_cards.count(remaining_cards[1]) == 2):
                temp_score = 2
            else:
                temp_score = 1
        else:
            temp_score = 0
        if temp_score > score:
            score = temp_score
    return score


def compare_equivalent_hands(hand_1: str, hand_2: str) -> int:
    values = {
        'T': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    for card_1, card_2 in zip(list(hand_1), list(hand_2)):
        if int(values.get(card_1, card_1)) > int(values.get(card_2, card_2)):
            return 1
        elif int(values.get(card_1, card_1)) < int(values.get(card_2, card_2)):
            return 2


def part_one(str_input: str):
    hands = []
    for line in str_input.split('\n'):
        hand = line.split()[0]
        bid = int(line.split()[1].strip())
        hands.append([hand, bid, hand_score(hand)])

    for i in range(len(hands)):
        for j in range(len(hands) - i - 1):
            if (hands[j][2] > hands[j+1][2]) or \
                (hands[j][2] == hands[j+1][2] and compare_equivalent_hands(hands[j][0], hands[j+1][0]) == 1):
                hands[j], hands[j+1] = hands[j+1], hands[j]

    score = list(map(lambda hand: hand[1] * (hands.index(hand) + 1), hands))
    return sum(score)


def test_part_one():
    assert hand_score("TTT98") == 3
    assert hand_score("33332") == 5
    assert hand_score("2AAAA") == 5
    assert compare_equivalent_hands("33332", "2AAAA") == 1
    assert part_one("32T3K 765") == 765
    assert part_one("""32T3K 765
T55J5 684""") == 765 + 2*684
    assert part_one("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""") == 6440


# ----- PART TWO -----


CARDS = ['A', 'K', 'Q', 'T'] + [str(num) for num in list(range(2,10))]


def hand_score_v2(hand: str) -> int:
    score = 0
    jokers = [index for index, card in enumerate(list(hand)) if card == 'J']
    if jokers:
        joker_options = list(product(CARDS, repeat = len(jokers)))
        for joker_option in joker_options:
            temp_hand = hand
            for joker, option in zip(jokers, joker_option):
                temp_hand = temp_hand[:joker] + option + temp_hand[joker+1:]
            temp_score = hand_score(temp_hand)
            score = max([score, temp_score])
    else:
        score = hand_score(hand)
    return score


def compare_equivalent_hands_v2(hand_1: str, hand_2: str) -> int:
    values = {
        'T': 10,
        'J': 1,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    for card_1, card_2 in zip(list(hand_1), list(hand_2)):
        if int(values.get(card_1, card_1)) > int(values.get(card_2, card_2)):
            return 1
        elif int(values.get(card_1, card_1)) < int(values.get(card_2, card_2)):
            return 2


def part_two(str_input: str):
    hands = []
    for line in str_input.split('\n'):
        hand = line.split()[0]
        bid = int(line.split()[1].strip())
        hands.append([hand, bid, hand_score_v2(hand)])

    for i in range(len(hands)):
        for j in range(len(hands) - i - 1):
            if (hands[j][2] > hands[j+1][2]) or \
                (hands[j][2] == hands[j+1][2] and compare_equivalent_hands_v2(hands[j][0], hands[j+1][0]) == 1):
                hands[j], hands[j+1] = hands[j+1], hands[j]

    score = list(map(lambda hand: hand[1] * (hands.index(hand) + 1), hands))
    return sum(score)


def test_part_two():
    assert hand_score_v2("QJJQ2") == 5
    assert part_two("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""") == 5905


# --------------------


if __name__ == "__main__":
    print(part_one(read_data("day_7.txt")))
    print(part_two(read_data("day_7.txt")))