#!/usr/bin/env python3

from functools import wraps
from pathlib import Path
from typing import Callable
from urllib.request import Request, urlopen

YEAR = 2023
INPUT_URL_TEMPLATE = f"https://adventofcode.com/{YEAR}/day/{{day}}/input"
INPUT_FILE_TEMPLATE = "inputs/day{day:02}.txt"

def fetch_input(*, day: int) -> str:
    """Download input file for the website. Needs session cookie in './cookie'"""
    session_id = Path("cookie").read_text().strip()
    req = Request(INPUT_URL_TEMPLATE.format(day=day))
    req.add_header("Cookie", f"session={session_id}")
    return urlopen(req).read().decode()


def get_input(*, day: int) -> str:
    """Get input for given day from existing file or download if needed."""
    path = Path(INPUT_FILE_TEMPLATE.format(day=day))
    if not path.is_file():
        print(f"Downloading {path}...")
        path.write_text(fetch_input(day=day))
    return path.read_text()


def aoc(*, day: int, example: str | tuple[str, ...]):
    if not isinstance(example, tuple):
        example = (example,)
    def solution[T: int | str](*, part: int, expected: T | tuple[T, ...]):
        if not isinstance(expected, tuple):
            expected = (expected,)
        def attempt(fn: Callable[[str], T]):
            any_failed = False
            for example_, expected_ in zip(example, expected):
                result = fn(example_.strip())
                any_failed |= result != expected_
                print(f"### Part {part} example:  {result} {'✅' if result == expected_ else f'!= {expected_} ❌'}\n")
            if not any_failed:
                result = fn(get_input(day=day).strip())
                print(f"### Part {part} solution: {result}\n")
        return attempt
    return solution



def print_args(fn):
    """Utility decorator for debugging.
    Prints arguments and result of each call of the decorated function.
    """
    @wraps(fn)
    def wrapped(*args):
        result = fn(*args)
        print(*args, "->", result)
        return result
    return wrapped
