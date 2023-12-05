#!/usr/bin/env python3

import re
from dataclasses import dataclass
from operator import mul
from functools import reduce

from aoc import aoc

attempt = aoc(day=3, example="""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""")


def find_part_numbers(grid: list[str]):
    symbol_pattern = re.compile(r"[^.0-9]")
    max_row = len(grid) - 1
    max_column = len(grid[0]) - 1
    for row, line in enumerate(grid):
        for match in re.finditer(r"\d+", line):
            start = max(0, match.start() - 1)
            end = min(max_column, match.end())
            if ((row > 0 and symbol_pattern.search(grid[row - 1][start:end+1]))
                or symbol_pattern.match(grid[row][start])
                or symbol_pattern.match(grid[row][end])
                or (row < max_row and symbol_pattern.search(grid[row + 1][start:end+1]))
                ):
                yield int(match[0])

@attempt(part=1, expected=4361)
def solve_1(input):
    grid = input.split("\n")
    return sum(find_part_numbers(grid))


@dataclass(frozen=True)
class Number:
    value: int
    row: int
    start: int
    end: int

@dataclass(frozen=True)
class Star:
    row: int
    column: int

def find_numbers(grid: list[str]):
    for row, line in enumerate(grid):
        for match in re.finditer(r"\d+", line):
            yield Number(
                value=int(match[0]),
                row=row,
                start=match.start(),
                end=match.end() - 1,
            )

def find_stars(grid: list[str]):
    for row, line in enumerate(grid):
        for column, char in enumerate(line):
            if char == "*":
                yield Star(row, column)

def find_gears(grid: list[str]):
    numbers = set(find_numbers(grid))
    stars = set(find_stars(grid))
    for star in stars:
        adjacent_numbers = {n for n in numbers if abs(star.row - n.row) <= 1 and n.start - 1 <= star.column <= n.end + 1}
        if len(adjacent_numbers) == 2:
            yield reduce(mul, (n.value for n in adjacent_numbers))

@attempt(part=2, expected=467835)
def solve_2(input):
    return sum(find_gears(input.split("\n")))
