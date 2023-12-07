#!/usr/bin/env python3

import re
from typing import Iterable, Literal, Sequence
import math
from aoc import aoc
from itertools import cycle

attempt = aoc(day=8, example=(
"""
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""",
"""
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""",
))

type Network = dict[str, tuple[str, str]]
type Instruction = Literal[0, 1]

def parse_network(input: str) -> Network:
    return {
        match[1]: (match[2], match[3])
        for match in re.finditer(r"(\w{3}) = \((\w{3}), (\w{3})\)", input)
    }

@attempt(part=1, expected=(2, 6))
def solve_1(input: str):
    instructions: Iterable[Instruction] = cycle(0 if instr == "L" else 1 for instr in input.split("\n", 1)[0])
    network = parse_network(input)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        current_node = network[current_node][next(instructions)]
        steps += 1

    return steps


attempt = aoc(day=8, example="""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""")

def get_distance(network: Network, start_node: str, instructions: Sequence[Instruction]):
    current_node = start_node
    steps = 0
    instructions_cycle = iter(cycle(instructions))
    while not current_node.endswith("Z"):
        current_node = network[current_node][next(instructions_cycle)]
        steps += 1
    return steps

@attempt(part=2, expected=6)
def solve_2(input: str):
    instructions = tuple(0 if instr == "L" else 1 for instr in input.split("\n", 1)[0])
    network = parse_network(input)

    start_nodes = tuple(key for key in network.keys() if key.endswith("A"))

    # This works only because the input has additional properties not specified
    # in the problem description (not cool, imho).
    # * Each start node reaches exactly one end node.
    # * Once an end node is reached, it will be reached again after the same
    #   number of steps.
    # Once you find this out via trial and error it's clear the combined cycles
    # repeat after LCM steps.
    return math.lcm(*(get_distance(network, node, instructions) for node in start_nodes))
