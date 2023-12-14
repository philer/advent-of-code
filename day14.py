#!/usr/bin/env python3

from collections.abc import Sequence
from aoc import aoc

attempt = aoc(day=14, example=
"""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""",
)


type Grid = tuple[str, ...]


def transpose(grid: Sequence[str]) -> Grid:
    return tuple("".join(line[idx] for line in grid) for idx in range(len(grid[0])))


def rot90(grid: Sequence[str]) -> Grid:
    return tuple(reversed(transpose(grid)))


def roll_line(row: Sequence[str]) -> list[str]:
    row = list(row)
    current_stop = 0
    for idx in range(len(row)):
        match row[idx]:
            case ".":
                pass
            case "#":
                current_stop = idx + 1
            case "O":
                if idx == current_stop:
                    current_stop = idx + 1
                else:
                    row[idx] = "."
                    row[current_stop] = "O"
                    current_stop += 1
    return row


def tilt(grid: Sequence[str]) -> list[str]:
    grid = list(grid)
    for row in range(len(grid)):
        grid[row] = "".join(roll_line(grid[row]))
    return grid


def get_line_value(line: str) -> int:
    return sum(value for value, item in zip(range(len(line), 0, -1), line) if item == "O")


@attempt(part=1, expected=136)
def solve_1(input: str):
    grid = transpose(tuple(input.splitlines()))
    return sum(map(get_line_value, tilt(grid)))


@attempt(part=2, expected=64)
def solve_2(input: str):
    grid = transpose(tuple(input.splitlines()))
    known_grids = dict[Grid, int]()

    repeated_at_idx = -1
    for idx in range(1_000_000_000):
        for _ in range(4):
            grid = rot90(tilt(grid))
        # print(*transpose(grid), sep="\n", end="\n\n")

        if grid in known_grids:
            repeated_at_idx = idx
            break
        known_grids[grid] = idx

    repeated_idx = known_grids[grid]
    cycle_length = repeated_at_idx - repeated_idx
    remaining_cycles = (1_000_000_000 - repeated_idx - 1) % cycle_length

    final_grid = next(grid for grid, idx in known_grids.items()
                      if idx == repeated_idx + remaining_cycles)

    return sum(map(get_line_value, final_grid))
