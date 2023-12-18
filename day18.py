#!/usr/bin/env python3

from collections import deque
from collections.abc import Iterable
from enum import Enum
from typing import Literal
from aoc import aoc

attempt = aoc(day=18, example=
r"""
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""",
)


type Grid = tuple[tuple[int, ...], ...]
type Point = tuple[int, int]

class D(tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]], Enum):
    DOWN = 1, 0
    RIGHT = 0, 1
    UP = -1, 0
    LEFT = 0, -1

    def move(self, point: Point, steps: int=1) -> Point:
        return point[0] + self[0] * steps, point[1] + self[1] * steps


def parse_1(input: str) -> Iterable[tuple[D, int]]:
    for line in input.splitlines():
        direction, steps, _ = line.split(" ")
        yield (
            {"D": D.DOWN, "R": D.RIGHT, "U": D.UP, "L": D.LEFT}[direction],
            int(steps),
        )


def dig_loop(instructions: Iterable[tuple[D, int]]) -> Iterable[Point]:
    position = 0, 0
    yield position
    for direction, steps in instructions:
        for _ in range(steps):
            position = direction.move(position)
            yield position


def dig_inside_loop(loop: set[Point]) -> set[Point]:
    # Crawl the outside of the loop
    # with a one tile gap around to ensure a fully connected area.
    min_row = min(row for row, _ in loop) - 1
    min_column = min(column for _, column in loop) - 1
    max_row = max(row for row, _ in loop) + 1
    max_column = max(column for _, column in loop) + 1
    outside = set[Point]()
    to_check = deque([(min_row, min_column)])
    while to_check:
        check = to_check.pop()
        for neighbour in (direction.move(check) for direction in D):
            if (min_row <= neighbour[0] <= max_row
                and min_column <= neighbour[1] <= max_column
                and neighbour not in loop
                and neighbour not in outside):
                outside.add(neighbour)
                to_check.append(neighbour)

    # invert the result to get only the inside
    all_points: set[Point] = {(row, column)
                              for row in range(min_row, max_row + 1)
                              for column in range(min_column, max_column + 1)}
    return all_points - loop - outside


@attempt(part=1, expected=62)
def solve_1(input: str):
    loop = set(dig_loop(parse_1(input)))
    inside = set(dig_inside_loop(loop))
    return len(loop | inside)


def parse_2(input: str) -> Iterable[tuple[D, int]]:
    for line in input.splitlines():
        _, hex_digits = line.split("#")
        yield (
            {"0": D.RIGHT, "1": D.DOWN, "2": D.LEFT, "3": D.UP}[hex_digits[5]],
            int(hex_digits[:5], base=16),
        )


@attempt(part=2, expected=952_408_144_115)
def solve_2(input: str):
    return 0
