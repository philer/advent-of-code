#!/usr/bin/env python3

from typing import Sequence
from aoc import aoc

attempt = aoc(day=11, example=
"""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""",
)

def find_galaxies(input: str, gap_scale: int):
    grid = tuple(input.split("\n"))

    galaxy_columns = {column
                      for line in grid
                      for column, char in enumerate(line)
                      if char == "#"}

    row_stretch = 0
    for row, line in enumerate(grid):
        row_has_galaxies = False
        column_stretch = 0
        for column, char in enumerate(line):
            if char == "#":
                row_has_galaxies = True
                yield row + row_stretch, column + column_stretch
            elif column not in galaxy_columns:
                column_stretch += gap_scale - 1
        if not row_has_galaxies:
            row_stretch += gap_scale - 1

def find_distances(galaxies: Sequence[tuple[int, int]]):
    for idx, start in enumerate(galaxies):
        for end in galaxies[idx + 1:]:
            yield end[0] - start[0] + abs(end[1] - start[1])

@attempt(part=1, expected=374)
def solve_1(input: str):
    return sum(find_distances(tuple(find_galaxies(input, gap_scale=2))))

@attempt(part=2, expected=())
def solve_2(input: str):
    return sum(find_distances(tuple(find_galaxies(input, gap_scale=1_000_000))))
