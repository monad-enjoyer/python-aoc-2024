from sys import argv


def is_safe(report: list[int]) -> int:
    if report[0] > report[1]:
        sign = -1
    elif report[0] < report[1]:
        sign = 1
    else:
        return 0
    least, most = min(1 * sign, 3 * sign), max(1 * sign, 3 * sign)
    result =  1 if all(least <= report[i+1] - report[i] <= most for i in range(len(report)-1)) else 0
    return result


def part1(lines: list[str]) -> None:
    lines = [list(map(int, line.split())) for line in lines]
    print("part1:", sum(map(is_safe, lines))) 


def part2(lines: list[str]) -> None:
    lines = [list(map(int, line.split())) for line in lines]
    total = 0
    for line in lines:
        if is_safe(line):
            total += 1
        else:
            for i in range(len(line)):
                if is_safe(line[0:i]+line[i+1:]):
                    total += 1
                    break
    print("part2:", total)


def main() -> None:
    path = "input.txt"
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        lines = [line.rstrip() for line in f]
    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()

