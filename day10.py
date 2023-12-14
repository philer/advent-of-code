#!/usr/bin/env python3

from collections import deque
from collections.abc import Iterator
from enum import Enum
from typing import Literal

from aoc import aoc

attempt = aoc(day=10, example=(
"""
.....
.S-7.
.|.|.
.L-J.
.....
""",
"""
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""",
"""
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""",
"""
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""",
))

type Grid = tuple[str, ...]
type Point = tuple[int, int]
type Direction = tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]]

class D(tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]], Enum):
    DOWN = 1, 0
    RIGHT = 0, 1
    UP = -1, 0
    LEFT = 0, -1

def find_adjacent_pipe_directions(grid: Grid, at: Point) -> Iterator[Direction]:
    for direction, connections in (D.DOWN, "|LJ"), (D.RIGHT, "-J7"), (D.UP, "|7F"), (D.LEFT, "-FL"):
        row, col = at[0] + direction[0], at[1] + direction[1]
        if grid[row][col] in connections:
            yield direction

def get_loop(grid: Grid, start: Point, direction: Direction):
    row, col = start[0] + direction[0], start[1] + direction[1]
    yield row, col
    while grid[row][col] != "S":
        match grid[row][col], direction:
            case ("|", D.DOWN) | ("|", D.UP) | ("-", D.LEFT) | ("-", D.RIGHT):
                pass
            case "L", D.DOWN:
                direction = D.RIGHT
            case "L", D.LEFT:
                direction = D.UP
            case "F", D.UP:
                direction = D.RIGHT
            case "F", D.LEFT:
                direction = D.DOWN
            case "J", D.DOWN:
                direction = D.LEFT
            case "J", D.RIGHT:
                direction = D.UP
            case "7", D.UP:
                direction = D.LEFT
            case "7", D.RIGHT:
                direction = D.DOWN
            case _:
                raise RuntimeError("Cannot enter pipe from this direction")
        row, col = row + direction[0], col + direction[1]
        yield row, col

@attempt(part=1, expected=(4, 4, 8, 8))
def solve_1(input: str):
    grid = tuple(input.split("\n"))
    start = divmod("".join(grid).index("S"), len(grid[0]))
    return sum(1 for _ in get_loop(grid, start, next(find_adjacent_pipe_directions(grid, start)))) // 2

attempt = aoc(day=10, example=(
"""
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""",
"""
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
""",
"""
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""",
"""
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
))

def get_zoomed_grid(grid, start):
    """What do you mean, "memory efficiency"?"""
    zoomed = [list("." * 3 * len(grid[0])) for _ in range(3 * len(grid))]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            zoomed_row, zoomed_col = row * 3 + 1, col * 3 + 1
            zoomed[zoomed_row][zoomed_col] = grid[row][col]
            match grid[row][col]:
                case "|":
                    zoomed[zoomed_row - 1][zoomed_col] = "|"
                    zoomed[zoomed_row + 1][zoomed_col] = "|"
                case "-":
                    zoomed[zoomed_row][zoomed_col - 1] = "-"
                    zoomed[zoomed_row][zoomed_col + 1] = "-"
                case "F":
                    zoomed[zoomed_row + 1][zoomed_col] = "|"
                    zoomed[zoomed_row][zoomed_col + 1] = "-"
                case "7":
                    zoomed[zoomed_row + 1][zoomed_col] = "|"
                    zoomed[zoomed_row][zoomed_col - 1] = "-"
                case "J":
                    zoomed[zoomed_row - 1][zoomed_col] = "|"
                    zoomed[zoomed_row][zoomed_col - 1] = "-"
                case "L":
                    zoomed[zoomed_row - 1][zoomed_col] = "|"
                    zoomed[zoomed_row][zoomed_col + 1] = "-"

    # Attach start-adjacent pipes
    row, col = start[0] * 3 + 1, start[1] * 3 + 1
    zoomed[row][col] = "S"
    for d_row, d_col in find_adjacent_pipe_directions(grid, start):
        zoomed[row + d_row][col + d_col] = "|" if d_row else "-"

    return tuple(map("".join, zoomed))

@attempt(part=2, expected=(4, 4, 8, 10))
def solve_2(input):
    grid = tuple(input.split("\n"))
    start = divmod("".join(grid).index("S"), len(grid[0]))
    start_direction = next(find_adjacent_pipe_directions(grid, start))
    loop = set(get_loop(grid, start, start_direction))

    # To work around the issue of parallel pipes with no gap in between,
    # generate a higher resolution grid. This way all non-loop squares are
    # connected by empty space and a simple neighbor search can find all
    # outside squares without having to follow zero-width pathways.
    zoomed_grid = get_zoomed_grid(grid, start)
    zoomed_start = start[0] * 3 + 1, start[1] * 3 + 1
    zoomed_loop = set(get_loop(zoomed_grid, zoomed_start, start_direction))

    to_check = deque[Point]([(0, 0)])
    zoomed_outside: set[Point] = {(0, 0)}
    while to_check:
        check = to_check.pop()
        for direction in D:
            neighbor = check[0] + direction[0], check[1] + direction[1]
            try:
                # Check if we're still inside bounds
                zoomed_grid[neighbor[0]][neighbor[1]]
            except IndexError:
                continue
            if neighbor not in zoomed_outside and neighbor not in zoomed_loop:
                to_check.append(neighbor)
                zoomed_outside.add(neighbor)

    outside = {(row, col) for row in range(len(grid)) for col in range(len(grid[0]))
               if (row * 3 + 1, col * 3 + 1) in zoomed_outside}
    return len(grid) * len(grid[0]) - len(outside) - len(loop)
