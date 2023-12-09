#!/usr/bin/env python3

from collections.abc import Iterable
from functools import reduce

from aoc import aoc

attempt = aoc(day=9, example="""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""")

def parse(input: str):
    return (map(int, line.split(" ")) for line in input.split("\n"))

def get_last_prediction(ns: Iterable[int]) -> int:
    ns = tuple(ns)
    result = ns[-1]
    while len(set(ns)) > 1:
        ns = tuple(b - a for a, b in zip(ns[:-1], ns[1:]))
        result += ns[-1]
    return result

def get_first_prediction(ns: Iterable[int]) -> int:
    ns = tuple(ns)
    path = [ns[0]]
    while len(set(ns)) > 1:
        ns = tuple(b - a for a, b in zip(ns[:-1], ns[1:]))
        path.append(ns[0])
    return reduce(lambda result, n: n - result, reversed(path))

@attempt(part=1, expected=114)
def solve_1(input):
    return sum(map(get_last_prediction, parse(input)))

@attempt(part=2, expected=2)
def solve_2(input):
    return sum(map(get_first_prediction, parse(input)))


