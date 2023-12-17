#!/usr/bin/env python3

from collections import deque
from enum import Enum
from typing import Literal
from aoc import aoc

attempt = aoc(day=17, example=
r"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""",
)


type Grid = tuple[tuple[int, ...], ...]
type Point = tuple[int, int]

class D(tuple[Literal[-1, 0, 1], Literal[-1, 0, 1]], Enum):
    DOWN = 1, 0
    RIGHT = 0, 1
    UP = -1, 0
    LEFT = 0, -1


def parse(input: str) -> Grid:
    return tuple(tuple(map(int, line)) for line in input.splitlines())


def shortest_path(grid: Grid, start: Point, goal: Point, min_steps: int, max_steps: int) -> int:
    """Some weird variant of Dijkstra's algorithm"""
    width, height = len(grid[0]), len(grid)
    to_check = deque[tuple[Point, D, int]]([
        (start, D.DOWN, 0),
        (start, D.RIGHT, 0),
    ])
    shortest: dict[tuple[Point, D], tuple[Point, int]] = {}

    # use arbitrary simple path as a longest relevant path for optimization
    max_distance = sum(grid[x][x - 1] + grid[x][x] for x in range(1, len(grid)))
    while to_check:
        current, direction, distance = to_check.pop()
        point = current
        for steps in range(1, max_steps + 1):
            point = point[0] + direction[0], point[1] + direction[1]
            if not (0 <= point[0] < height and 0 <= point[1] < width):
                break
            distance += grid[point[0]][point[1]]
            if steps < min_steps:
                continue
            if point == goal:
                max_distance = distance
            if distance > max_distance:
                break
            if shortest.get((point, direction), ((0, 0), 2**64))[1] > distance:
                shortest[(point, direction)] = current, distance
                left = {D.DOWN: D.RIGHT, D.RIGHT: D.UP, D.UP: D.LEFT, D.LEFT: D.DOWN}[direction]
                to_check.append((point, left, distance))
                right =  {D.DOWN: D.LEFT, D.LEFT: D.UP, D.UP: D.RIGHT, D.RIGHT: D.DOWN}[direction]
                to_check.append((point, right, distance))
    return min(shortest[(goal, direction)][1] for direction in D if (goal, direction) in shortest)


@attempt(part=1, expected=102)
def solve_1(input: str):
    grid = parse(input)
    return shortest_path(
        grid=grid,
        start=(0, 0),
        goal=(len(grid) - 1, len(grid[0]) - 1),
        min_steps=1,
        max_steps=3,
    )


attempt = aoc(day=17, example=(
"""
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""",
"""
111111111111
999999999991
999999999991
999999999991
999999999991
"""
))


@attempt(part=2, expected=(94, 71))
def solve_2(input: str):
    grid = parse(input)
    return shortest_path(
        grid=grid,
        start=(0, 0),
        goal=(len(grid) - 1, len(grid[0]) - 1),
        min_steps=4,
        max_steps=10,
    )
