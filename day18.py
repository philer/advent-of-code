#!/usr/bin/env python3

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


def parse_2(input: str) -> Iterable[tuple[D, int]]:
    for line in input.splitlines():
        _, hex_digits = line.split("#")
        yield (
            {"0": D.RIGHT, "1": D.DOWN, "2": D.LEFT, "3": D.UP}[hex_digits[5]],
            int(hex_digits[:5], base=16),
        )


def get_hole_size(instructions: Iterable[tuple[D, int]]) -> int:
    interior = 0
    current = 0, 0
    for direction, steps in instructions:
        previous, current = current, direction.move(current, steps)
        if d_row := current[0] - previous[0]:
            interior += d_row * (previous[1] + 1)
            if d_row < 0:
                interior -= d_row
        elif (d_column := current[1] - previous[1]) < 0:
            interior -= d_column
    return interior + 1


@attempt(part=1, expected=62)
def solve_1(input: str):
    return get_hole_size(parse_1(input))


@attempt(part=2, expected=952_408_144_115)
def solve_2(input: str):
    return get_hole_size(parse_2(input))
