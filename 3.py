from math import prod
from functools import reduce
from sys import argv
import re


def part1(line: str) -> int:
    pattern = r"mul\(\d+,\d+\)"
    match = re.finditer(pattern, line)
    total = 0
    for x in match:
        slice = line[x.start() + 4: x.end() -1]
        this = prod(int(num) for num in slice.split(','))
        total += this
    return total

def part1_one_liner() -> int:
    return sum(map(lambda match: prod((int(num) for num in match.group()[4:-1].split(','))),re.finditer(r"mul\(\d+,\d+\)", open("input.txt").read().strip())))


def part2(line: str) -> int:
    pattern = r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))"
    match = re.finditer(pattern, line)
    should_mul = True
    total = 0
    for m in match:
        if m.group() == "do()":
            should_mul = True
        elif m.group() == "don't()":
            should_mul = False
        else:
            if not should_mul:
                continue
            slice = line[m.start() + 4: m.end() -1]
            this = prod(int(num) for num in slice.split(','))
            total += this
    return total

def part2_one_liner() -> int:
    return reduce(lambda tup, group: (tup[0], True) if group == "do()" else (tup[0], False) if group == "don't()" else tup if not tup[1] else (prod((int(num) for num in group[4:-1].split(',')))+tup[0], True),(match.group() for match in re.finditer(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", open("input.txt").read().strip())),(0, True))[0]

def main() -> None:
    path = "test.txt"
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        line = f.read().strip()
    print("part1:", part1(line))
    print("part2:", part2(line))
    print("part1 one liner:", part1_one_liner())
    print("part2 one liner:", part2_one_liner()) 

if __name__ == "__main__":
    main()
