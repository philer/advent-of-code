#!/usr/bin/env python3

with open("inputs/day01.txt", "r") as file:
    result = 0
    for line in file:
        digits = tuple(filter(str.isdigit, line))
        result += int(f"{digits[0]}{digits[-1]}")
    print(result)

