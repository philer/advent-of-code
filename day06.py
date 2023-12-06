#!/usr/bin/env python3

import re
from functools import reduce
from operator import mul

from aoc import aoc

attempt = aoc(day=6, example="""
Time:      7  15   30
Distance:  9  40  200
""")


def distance(total_time, wait_time):
    return (total_time - wait_time) * wait_time

SPACES_PATTERN = re.compile(r"\s+")

def parse(input):
    return zip(*(map(int, SPACES_PATTERN.split(line)[1:]) for line in input.split("\n")))

@attempt(part=1, expected=288)
def solve_1(input):
    races = list(parse(input))
    # simple optimization available: only check from start and end until the first hit
    # (maybe optimize with binary search)
    winning_options = (
        sum(1 for wait_time in range(1, total_time) if distance(total_time, wait_time) > best_distance)
        for total_time, best_distance in races
    )
    return reduce(mul, winning_options)


def parse_bad_kerning(input):
    return tuple(int("".join(SPACES_PATTERN.split(line)[1:])) for line in input.split("\n"))


@attempt(part=2, expected=71503)
def solve_2(input):
    total_time, best_distance = parse_bad_kerning(input)
    return sum(1 for wait_time in range(1, total_time) if distance(total_time, wait_time) > best_distance)