#!/usr/bin/env python3

from functools import reduce
from aoc import aoc


attempt = aoc(day=15, example="""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""")


def hash_(string: str):
    return reduce(lambda result, char: ((result + ord(char)) * 17) % 256, string, 0)


@attempt(part=1, expected=1320)
def solve_1(input: str):
    return sum(map(hash_, input.split(",")))


@attempt(part=2, expected=145)
def solve_2(input: str):
    boxes = tuple(dict() for _ in range(256))
    for op in input.split(","):
        if op.endswith("-"):
            label = op[:-1]
            boxes[hash_(label)].pop(label, 1337)  # default ignored to skip KeyError
        else:
            label, focus = op.split("=")
            boxes[hash_(label)][label] = int(focus)

    return sum(box_number * slot_number * focus
               for box_number, box in enumerate(boxes, start=1)
               for slot_number, focus in enumerate(box.values(), start=1))
