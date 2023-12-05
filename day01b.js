#!/usr/bin/env node

const { readFile } = require('fs/promises')

const EXAMPLE = `
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
`.trim()


const DIGITS = {
  "0": 0, "zero": 0,
  "1": 1, "one": 1,
  "2": 2, "two": 2,
  "3": 3, "three": 3,
  "4": 4, "four": 4,
  "5": 5, "five": 5,
  "6": 6, "six": 6,
  "7": 7, "seven": 7,
  "8": 8, "eight": 8,
  "9": 9, "nine": 9,
}

const solve = input =>
  input
    .trim()
    .split("\n")
    .reduce((sum, line) =>
      sum + +`${
          DIGITS[line.match(/zero|one|two|three|four|five|six|seven|eight|nine|[0-9]/)[0]]
        }${
          DIGITS[line.match(/.*(zero|one|two|three|four|five|six|seven|eight|nine|[0-9])/)[1]]
        }`,
      0
    )


console.log(solve(EXAMPLE))

readFile("inputs/day01.txt", { encoding: "utf8" })
  .then(solve)
  .then(console.log, console.error)
