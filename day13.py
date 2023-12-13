#!/usr/bin/env python3

from collections.abc import Sequence
from typing import cast
from aoc import aoc

attempt = aoc(day=13, example=
"""
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""",
)


def parse(input: str):
    return (img.split("\n") for img in input.split("\n\n"))

def transpose(grid: Sequence[str]):
    return tuple("".join(line[idx] for line in grid) for idx in range(len(grid[0])))

def find_horizontal_axis(image: Sequence[str]):
    for axis in range(1, len(image)):
        for top, bottom in zip(reversed(image[:axis]), image[axis:]):
            if top != bottom:
                break
        else:
            return axis

@attempt(part=1, expected=405)
def solve_1(input: str):
    return sum(
        find_horizontal_axis(transpose(image))
        or 100 * cast(int, find_horizontal_axis(image))
        for image in parse(input)
    )

def find_horizontal_axis_with_fix(image: Sequence[str]):
    for axis in range(1, len(image)):
        has_fixable_line_error = False
        for top, bottom in zip(reversed(image[:axis]), image[axis:]):
            diff = sum(1 for tp, bttm in zip(top, bottom) if tp != bttm)
            if diff > 1:
                break
            elif diff == 1:
                if has_fixable_line_error:
                    break
                has_fixable_line_error = True
        else:
            if has_fixable_line_error:
                return axis

@attempt(part=2, expected=400)
def solve_2(input: str):
    return sum(
        find_horizontal_axis_with_fix(transpose(image))
        or 100 * cast(int, find_horizontal_axis_with_fix(image))
        for image in parse(input)
    )
