from collections import Counter
from itertools import cycle
from sys import argv


def part1(path: str):
    left = []
    right = []
    with open(path) as f:
        for line in f:
            try:
                fields = line.strip().split()
                left.append(int(fields[0]))
                right.append(int(fields[1]))
            except ValueError:
                raise ValueError()
    assert len(left) == len(right), f"left length {len(left)} not equal to right length {len(right)}"
    left.sort(reverse=True)
    right.sort(reverse=True)
    total = 0
    while left:
        l, r = left.pop(), right.pop()
        total += max(l, r) - min(l, r)
    print(total)


def part2(path: str) -> None:
    #with open(path) as f:
    left = (int(line.split()[0]) for line in open(path))
    #with open(path) as f:
    right = Counter(int(line.split()[1]) for line in open(path))
    print(sum(map(lambda num: num * right[num], left)))


def part1_one_liner(path: str) -> None:
    print(sum(map(lambda tup: abs(tup[0] - tup[1]), zip(sorted(int(line.rstrip().split()[0]) for line in open(path)),sorted(int(line.rstrip().split()[1]) for line in open(path)),strict=True))))


def part2_one_liner(path: str) -> None:
    print(sum
          (map(lambda tup: tup[0] * tup[1][tup[0]], zip(sorted(int(line.rstrip().split()[0]) for line in open(path)),cycle([Counter(int(line.rstrip().split()[1]) for line in open(path)),]))))
          )
def main() -> None:
    if len(argv) == 2:
        path = argv[1]
    else:
        path = "input.txt"
    #part1(path)
    #part2(path)
    part1_one_liner(path)
    part2_one_liner(path)

    

if __name__ == "__main__":
    main()
