#!/usr/bin/env python3

from collections.abc import Iterable
from enum import IntEnum
from collections import Counter

from aoc import aoc

attempt = aoc(day=7, example="""
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""")

def parse(input: str) -> Iterable[tuple[str, int]]:
    return ((hand, int(bid)) for hand, bid in map(str.split, input.split("\n")))

class HT(IntEnum):
    """Hand type rank values"""
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

def get_hand_type(hand: str) -> int:
    match sorted(Counter(hand).values(), reverse=True):
        case [5]:
            return HT.FIVE_OF_A_KIND
        case [4, *_]:
            return HT.FOUR_OF_A_KIND
        case [3, 2]:
            return HT.FULL_HOUSE
        case [3, *_]:
            return HT.THREE_OF_A_KIND
        case [2, 2, *_]:
            return HT.TWO_PAIR
        case [2, *_]:
            return HT.ONE_PAIR
        case _:
            return HT.HIGH_CARD

CARD_VALUES = {card: value for value, card in enumerate("23456789TJQKA")}

def get_hand_value(hand: tuple[str, int]) -> tuple[int, ...]:
    return get_hand_type(hand[0]), *(CARD_VALUES[card] for card in hand[0])

@attempt(part=1, expected=6440)
def solve_1(input: str):
    hands = sorted(parse(input), key=get_hand_value)
    return sum(rank * bid for rank, (_, bid) in enumerate(hands, start=1))


def get_hand_type_jokers(hand: str) -> int:
    non_jokers = "".join(card for card in hand if card != "J")
    match get_hand_type(non_jokers), 5 - len(non_jokers):
        case hand_type, 0:
            return hand_type
        case HT.FOUR_OF_A_KIND, 1:
            return HT.FIVE_OF_A_KIND
        case HT.THREE_OF_A_KIND, 1:
            return HT.FOUR_OF_A_KIND
        case HT.THREE_OF_A_KIND, 2:
            return HT.FIVE_OF_A_KIND
        case HT.TWO_PAIR, 1:
            return HT.FULL_HOUSE
        case HT.ONE_PAIR, 1:
            return HT.THREE_OF_A_KIND
        case HT.ONE_PAIR, 2:
            return HT.FOUR_OF_A_KIND
        case HT.ONE_PAIR, 3:
            return HT.FIVE_OF_A_KIND
        case HT.HIGH_CARD, 1:
            return HT.ONE_PAIR
        case HT.HIGH_CARD, 2:
            return HT.THREE_OF_A_KIND
        case HT.HIGH_CARD, 3:
            return HT.FOUR_OF_A_KIND
        case HT.HIGH_CARD, 4 | 5:
            return HT.FIVE_OF_A_KIND
    raise ValueError

CARD_VALUES_JOKERS = {card: value for value, card in enumerate("J23456789TQKA")}

def get_hand_value_jokers(hand: tuple[str, int]) -> tuple[int, ...]:
    card_values = (CARD_VALUES_JOKERS[card] for card in hand[0])
    return get_hand_type_jokers(hand[0]), *card_values

@attempt(part=2, expected=5905)
def solve_2(input: str):
    hands = sorted(parse(input), key=get_hand_value_jokers)
    return sum(rank * bid for rank, (_, bid) in enumerate(hands, start=1))
