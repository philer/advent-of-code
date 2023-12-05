#!/usr/bin/env python3

from aoc import aoc

attempt = aoc(day=1, example="""
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""")

@attempt(part=1, expected=142)
def solve_1(input):
    result = 0
    for line in input.split("\n"):
        digits = tuple(filter(str.isdigit, line))
        result += int(f"{digits[0]}{digits[-1]}")
    return result
