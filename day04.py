#!/usr/bin/env python3

import re
from functools import cache

from aoc import aoc

attempt = aoc(day=4, example="""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""")

SPACES_PATTERN = re.compile(r"\s+")

def parse_card(card):
    return tuple(map(SPACES_PATTERN.split, re.split(r":\s+", card)[1].split(" | ")))

@cache
def evaluate_card(card):
    winning, own = parse_card(card)
    return len(set(winning) & set(own))

@attempt(part=1, expected=13)
def solve_1(input):
    cards = input.strip().split("\n")
    return sum(2 ** (n - 1) for n in map(evaluate_card, cards) if n)

@attempt(part=2, expected=30)
def solve_2(input):
    cards = input.strip().split("\n")
    counters = [1 for _ in cards]
    for idx, card in enumerate(cards):
        # print(idx, range(idx, min(idx + evaluate_card(card), len(cards))))
        for bonus_idx in range(idx, min(idx + evaluate_card(card), len(cards))):
            counters[bonus_idx + 1] += counters[idx]
    # print(counters)
    return sum(counters)
