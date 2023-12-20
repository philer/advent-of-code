#!/usr/bin/env python3

from collections import Counter, deque
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from operator import mul
from typing import Literal, Optional

from aoc import aoc


attempt = aoc(day=20, example=(
"""
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""",
"""
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""))


type PulseValue = Literal["low", "high"]
type Pulse = tuple[PulseValue, str, str]

@dataclass(kw_only=True)
class BaseModule:
    name: str
    outputs: tuple[str, ...]

@dataclass(kw_only=True)
class FlipFlop(BaseModule):
    on: bool = False

@dataclass(kw_only=True)
class Conjunction(BaseModule):
    inputs: dict[str, PulseValue] = field(default_factory=dict)

@dataclass(kw_only=True)
class Broadcast(BaseModule):
    pass

type Module = FlipFlop | Conjunction | Broadcast


def parse(input: str):
    for line in input.splitlines():
        if not line or line.startswith("#"):  # comment
            continue
        name, outputs = line.split(" -> ")
        outputs = tuple(outputs.split(", "))
        match name[0]:
            case "%":
                yield FlipFlop(name=name[1:], outputs=outputs)
            case "&":
                yield Conjunction(name=name[1:], outputs=outputs)
            case "b":
                yield Broadcast(name=name, outputs=outputs)
            case _:
                raise ValueError(f"Unexpected module description '{line}'")


def init_conjunctions(network: dict[str, Module]):
    for name, module in network.items():
        for output in module.outputs:
            match network.get(output):
                case Conjunction(inputs=inputs):
                    inputs[name] = "low"


def simulate(network: dict[str, Module]):
    pulses: deque[Pulse] = deque([("low", "button", "broadcaster")])
    while pulses:
        yield (pulse := pulses.popleft())
        value, from_module, to_module = pulse
        # print(f"\t{from_module} -{value}-> {to_module}")
        match module := network.get(to_module):  # ignore KeyError "output"
            case FlipFlop(name=name, on=on, outputs=outputs):
                if value == "low":
                    module.on = not on
                    pulses.extend(("low" if on else "high", name, output) for output in outputs)

            case Conjunction(name=name, inputs=inputs, outputs=outputs):
                module.inputs = {**inputs, from_module: value}
                value = "high" if "low" in module.inputs.values() else "low"
                pulses.extend((value, name, output) for output in outputs)

            case Broadcast(name=name, outputs=outputs):
                pulses.extend((value, name, output) for output in outputs)


@attempt(part=1, expected=(32000000, 11687500))
def solve_1(input: str):
    network = {module.name: module for module in parse(input)}
    init_conjunctions(network)
    pulses = Counter(pulse[0] for pulse in chain.from_iterable(simulate(network) for _ in range(1000)))
    return pulses["low"] * pulses["high"]


@attempt(part=2, expected=())
def solve_2(input: str):
    # Doesn't work
    network = {module.name: module for module in parse(input)}
    init_conjunctions(network)
    for i in range(100_000):
        if i % 10_000 == 0:
            print(i)
        for value, _, to_module in simulate(network):
            if to_module == "rx" and value == "low":
                return i + 1
