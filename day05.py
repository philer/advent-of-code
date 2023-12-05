#!/usr/bin/env python3

from dataclasses import dataclass
from functools import reduce
from itertools import batched, chain

from aoc import aoc

attempt = aoc(day=5, example="""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""")


def parse_seeds(lines):
    return map(int, lines[0].split(": ")[1].split(" "))

def parse_seed_ranges(lines):
    ns = tuple(parse_seeds(lines))
    for start, length in batched(ns, 2):
        yield range(start, start + length)

@dataclass
class Mapping:
    range_pairs: list[tuple[range, range]]

    def get(self, n: int) -> int:
        for src, dest in self.range_pairs:
            if n in src:
                return dest[n - src.start]
        return n

    def resolve(self, rng: range):
        for src, dest in self.range_pairs:
            if overlap := range(max(rng.start, src.start), min(rng.stop, src.stop)):
                if left := range(rng.start, src.start):
                    yield left
                yield range(dest[overlap.start - src.start], dest[overlap.stop - 1 - src.start] + 1)
                if not (rng := range(src.stop, rng.stop)):
                    return
        yield rng

def parse_mappings(lines):
    range_pairs = []
    for line in lines[3:]:
        if not line:
            continue
        try:
            dest_start, src_start, length = map(int, line.split(" "))
            range_pairs.append((range(src_start, src_start + length), range(dest_start, dest_start + length)))
        except ValueError:
            yield Mapping(range_pairs)
            range_pairs = []
    yield Mapping(range_pairs)

@attempt(part=1, expected=35)
def solve_1(input):
    lines = input.strip().split("\n")
    seeds = parse_seeds(lines)
    mappings = list(parse_mappings(lines))
    return min(
        reduce(
            lambda current, mapping: mapping.get(current),
            mappings,
            seed,
        )
        for seed in seeds
    )

@attempt(part=2, expected=46)
def solve_2(input):
    lines = input.strip().split("\n")
    seed_ranges = parse_seed_ranges(lines)
    mappings = list(parse_mappings(lines))

    ranges = reduce(
        lambda current_ranges, mapping: chain.from_iterable(map(mapping.resolve, current_ranges)),
        mappings,
        seed_ranges,
    )
    return min(rng.start for rng in ranges)
