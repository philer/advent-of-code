#!/usr/bin/env python3

import re
from functools import reduce
from operator import mul

EXAMPLE = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip()


ZERO_SET = {"red": 0, "green": 0, "blue": 0}

def parse(lines: str):
    for line in lines.strip().split("\n"):
        matches = re.findall(r"(\d+) (red|green|blue)(,|;|$)", line)
        sets = []
        current_set = {**ZERO_SET}
        for count, color, delimiter in matches:
            current_set[color] = int(count)
            if delimiter != ",":
                sets.append(current_set)
                current_set = {**ZERO_SET}
        yield sets

def find_invalid(lines: str, maxima: dict):
    for idx, game in enumerate(parse(lines)):
        if not any(maxima[color] < count for colorset in game for color, count in colorset.items()):
            yield idx + 1

def solve_1(lines: str, maxima: dict):
    return sum(find_invalid(lines, maxima))

def solve_2(lines: str):
    result = 0
    for game in parse(lines):
        min_set = {color: max(gameset[color] for gameset in game) for color in ("red", "green", "blue")}
        power = reduce(mul, min_set.values())
        result += power
    return result


print("Part 1 example:", solve_1(EXAMPLE, { "red": 12, "green": 13, "blue": 14}))
with open("inputs/day02.txt", "r") as file:
    print("Part 1 solution:", solve_1(open("inputs/day02.txt", "r").read(), { "red": 12, "green": 13, "blue": 14}))

print("Part 2 example:", solve_2(EXAMPLE))
with open("inputs/day02.txt", "r") as file:
    print("Part 2 solution:", solve_2(open("inputs/day02.txt", "r").read()))
