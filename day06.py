#!/usr/bin/env python3

import re
from functools import reduce
from operator import mul
from math import sqrt, floor, ceil

from aoc import aoc

attempt = aoc(day=6, example="""
Time:      7  15   30
Distance:  9  40  200
""")


SPACES_PATTERN = re.compile(r"\s+")

def parse(input):
    return zip(*(map(int, SPACES_PATTERN.split(line)[1:]) for line in input.split("\n")))

def get_winning_options_count(total_time: int, best_distance: int):
    # Brute force approach
    # Available optimization: only check from start and end until
    #   -> could be further optimized with binary search
    # return sum(1 for wait_time in range(1, total_time) if (total_time - wait_time) * wait_time > best_distance)

    # Math approach: Solve a quadratic (in)equation
    # (total_time - wait_time) * wait_time > best_distance
    # (t - w) * w > d
    # tw - w² > d
    # -1w² + tw - d > 0
    # This is a quadratic function in w. Based on the given problem its graph
    # is an upwards bending parabola with zeros at the score to beat.
    #
    # Solutions:
    # w1 = (-t + sqrt(t² - 4d)) / -2
    # w1 = (t - sqrt(t² - 4d)) / 2
    # w2 = (t + sqrt(t² - 4d)) / 2
    # -> score is beaten between w2 and w1

    # has solutions if t² - 4d > 0
    det = total_time ** 2 - 4 * best_distance
    if det < 0:
        return 0

    # calculate zeros
    w1 = .5 * (total_time - sqrt(det))
    w2 = .5 * (total_time + sqrt(det))

    # Exact hits do not count as "beating" the record
    if w1 == int(w1): w1 += 1
    if w2 == int(w2): w2 -= 1

    return floor(w2) - ceil(w1) + 1

@attempt(part=1, expected=288)
def solve_1(input):
    races = list(parse(input))
    return reduce(mul, (get_winning_options_count(total_time, best_distance) for total_time, best_distance in races))


def parse_bad_kerning(input):
    return tuple(int("".join(SPACES_PATTERN.split(line)[1:])) for line in input.split("\n"))


@attempt(part=2, expected=71503)
def solve_2(input):
    return get_winning_options_count(*parse_bad_kerning(input))
