#!/usr/bin/env python3

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from functools import reduce
from operator import mul
from typing import Literal, Optional

from aoc import aoc


attempt = aoc(day=19, example=
r"""
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""",
)


type Part = dict[str, int]
type PartRange = dict[str, range]


@dataclass(frozen=True)
class Rule:
    goto: str
    predicate: Callable[[Part], bool]
    predicate_parts: Optional[tuple[str, Literal[">", "<"], int]] = None


@dataclass(frozen=True)
class Workflow:
    name: str
    rules: tuple[Rule, ...]


TRUE = lambda _: True

def parse_rule(rule_def: str) -> Rule:
    if ":" in rule_def:
        predicate_def, goto = rule_def.split(":")
        category = predicate_def[0]
        operator = predicate_def[1]
        value = int(predicate_def[2:])
        match operator:
            case ">":
                predicate = lambda part: part[category] > value
            case "<":
                predicate = lambda part: part[category] < value
            case _:
                raise ValueError(f"Unexpected operation in rule '{rule_def}'")
        return Rule(goto, predicate, (category, operator, value))
    else:
        return Rule(rule_def, TRUE)


def parse_workflows(input: str) -> Iterable[Workflow]:
    for workflow_def in input.splitlines():
        name, rest = workflow_def.split("{")
        rule_defs = rest[:-1].split(",")
        yield Workflow(name, tuple(map(parse_rule, rule_defs)))


def parse_parts(input: str) -> Iterable[Part]:
    for part_def in input.splitlines():
        yield {cat: int(value) for cat, value
               in (item.split("=") for item in part_def[1:-1].split(","))}


def process_part(workflows: dict[str, Workflow], part: Part) -> bool:
    next_workflow = "in"
    while True:
        next_workflow = next(rule.goto for rule in workflows[next_workflow].rules if rule.predicate(part))
        match next_workflow:
            case "R":
                return False
            case "A":
                return True


def get_accepted_parts(workflows: Iterable[Workflow], parts: Iterable[Part]) -> Iterable[Part]:
    workflow_lookup = {workflow.name: workflow for workflow in workflows}
    for part in parts:
        if process_part(workflow_lookup, part):
            yield part


@attempt(part=1, expected=19114)
def solve_1(input: str):
    workflows_defs, part_defs = input.split("\n\n")
    accepted_parts = get_accepted_parts(parse_workflows(workflows_defs), parse_parts(part_defs))
    return sum(sum(part.values()) for part in accepted_parts)


def _follow_part_ranges(workflows: dict[str, Workflow], workflow_name: str, part: PartRange) -> Iterable[PartRange]:
    match workflow_name:
        case "A":
            yield part
        case "R":
            pass
        case _:
            for rule in workflows[workflow_name].rules:
                if rule.predicate_parts is None:
                    yield from _follow_part_ranges(workflows, rule.goto, part)
                else:
                    category, operator, value = rule.predicate_parts
                    match operator:
                        case "<":
                            matched_range = range(part[category].start, value)
                            remaining_range = range(value, part[category].stop)
                        case ">":
                            matched_range = range(value + 1, part[category].stop)
                            remaining_range = range(part[category].start, value + 1)
                    if matched_range:
                        yield from _follow_part_ranges(workflows, rule.goto, {**part, category: matched_range})
                    if remaining_range:
                        part = {**part, category: remaining_range}


def follow_part_ranges(workflows: Iterable[Workflow]) -> Iterable[PartRange]:
    yield from _follow_part_ranges(
        workflows={workflow.name: workflow for workflow in workflows},
        workflow_name="in",
        part={cat: range(1, 4001) for cat in "xmas"},
    )


@attempt(part=2, expected=167_409_079_868_000)
def solve_2(input: str):
    workflows = parse_workflows(input.split("\n\n")[0])
    part_ranges = follow_part_ranges(workflows)
    return sum(reduce(mul, map(len, parts.values())) for parts in part_ranges)
