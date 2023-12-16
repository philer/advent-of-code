#!/usr/bin/env python3

from collections import deque
from enum import Enum
from typing import Literal
from aoc import aoc

attempt = aoc(day=16, example=
r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""",
)


type Grid = tuple[str, ...]
type Point = tuple[int, int]
type Direction = tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]


class D(tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]], Enum):
    DOWN = 1, 0
    RIGHT = 0, 1
    UP = -1, 0
    LEFT = 0, -1


def reflect(direction: D, at: Literal["/", "\\"]) -> D:
    match direction, at:
        case D.DOWN, "/":
            return D.LEFT
        case D.DOWN, "\\":
            return D.RIGHT
        case D.RIGHT, "/":
            return D.UP
        case D.RIGHT, "\\":
            return D.DOWN
        case D.UP, "/":
            return D.RIGHT
        case D.UP, "\\":
            return D.LEFT
        case D.LEFT, "/":
            return D.DOWN
        case D.LEFT, "\\":
            return D.UP
        case _:
            raise ValueError("Unexpected reflection args")


def trace(grid: Grid, start: tuple[Point, D]) -> set[Point]:
    to_visit = deque([start])
    visited = set[Point]()
    visited_with_direction = set[tuple[Point, D]]()
    while to_visit:
        current = to_visit.pop()
        while current not in visited_with_direction:
            visited_with_direction.add(current)
            (row, column), direction = current
            if not (0 <= row < len(grid) and 0 <= column < len(grid[0])):
                break
            char = grid[row][column]
            visited.add((row, column))
            match char, direction:
                case ".", _:
                    current = (row + direction[0], column + direction[1]), direction
                case "/" | "\\", _:
                    new_dir = reflect(direction, char)
                    current = (row + new_dir[0], column + new_dir[1]), new_dir
                case ("|", D.UP | D.DOWN) | ("-", D.LEFT | D.RIGHT):
                    current = (row + direction[0], column + direction[1]), direction
                case "|" | "-", _:
                    dir_a, dir_b = (D.UP, D.DOWN) if char == "|" else (D.LEFT, D.RIGHT)
                    to_visit.append(((row + dir_a[0], column + dir_a[1]), dir_a))
                    to_visit.append(((row + dir_b[0], column + dir_b[1]), dir_b))
                    break
                case _:
                    raise ValueError("Unexpected grid square")
    return visited


@attempt(part=1, expected=46)
def solve_1(input: str):
    return len(trace(tuple(input.splitlines()), ((0, 0), D.RIGHT)))


@attempt(part=2, expected=51)
def solve_2(input: str):
    grid = tuple(input.splitlines())
    width, height = len(grid[0]), len(grid)
    starts = [((0, column), D.DOWN) for column in range(width)] \
           + [((height - 1, column), D.UP) for column in range(width)] \
           + [((row, 0), D.RIGHT) for row in range(height)] \
           + [((row, width - 1), D.LEFT) for row in range(height)]
    return max(len(trace(grid, start)) for start in starts)
