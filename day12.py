#!/usr/bin/env python3

from functools import cache
import re
from aoc import aoc

attempt = aoc(day=12, example=
"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""",
)

def parse(input: str):
    lines = input.split("\n")
    for line in lines:
        left, right = line.split(" ")
        runs = tuple(map(int, right.split(",")))
        yield left, runs


def simplify(record: str):
    return re.sub(r"\.+", ".", record).strip(".")


@cache
def new(record: str, runs: tuple[int, ...]):
    if not runs:
        return 0 if "#" in record else 1
    if not record:
        return 0
    if record[0] == ".":
        return new(record[1:], runs)

    run = runs[0]
    can_eat = len(record) >= run \
          and "." not in record[:run] \
          and (len(record) == run or record[run] != "#")

    match record[0], can_eat:
        case "#", True:
            return new(record[run + 1:], runs[1:])
        case "#", False:
            return 0
        case "?", True:
            return new(record[run + 1:], runs[1:]) + new(record[1:], runs)
        case "?", False:
            return new(record[1:], runs)
        case _:
            raise ValueError("Unexpected character")


@attempt(part=1, expected=21)
def solve_1(input: str):
    return sum(new(simplify(record), runs) for record, runs in parse(input))


@attempt(part=2, expected=525152)
def solve_2(input: str):
    return sum(new(simplify("?".join((record,) * 5)), runs * 5)
               for record, runs in parse(input))
