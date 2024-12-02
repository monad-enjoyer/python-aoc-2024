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


def is_safe_with_dampener(report: list[int], tolerance: int = 1) -> int:
    if report[0] > report[1]:
        sign = -1
    elif report[0] < report[1]:
        sign = 1
    else:
        return 0
    least, most = min(1 * sign, 3 * sign), max(1 * sign, 3 * sign)
    def run_report(report: list[int]) -> bool:
        for i, level in enumerate(report[0:-1]):
            if least <= report[i+1] - level <= most:
                continue
            return False
        return True
    has_bad = False
    popped = None
    for i, level in enumerate(report[0:-1]):
        if least <= report[i+1] - level <= most:
            continue
        has_bad = True
        nu_report = report[0:i] + report[i+1:]
        popped = f"{report[i]} at index {i}"
        break
    if not has_bad:
        print('passed', report)
        return 1
    for i, level in enumerate(nu_report[0:-1]):
        if least <= nu_report[i+1] - level <= most:
            continue
        print("bad", report, popped, nu_report)
        #print(report)
        return 0
    print("saved", report, popped, nu_report)
    return 1
        
    if bad_levels <= tolerance:
        return 1
    else:
        return 0


def part1(lines: list[str]) -> None:
    lines = [list(map(int, line.split())) for line in lines]
    #for line in lines:
    #print(is_safe(line), line)
    print(sum(map(is_safe, lines))) 


def part2(lines: list[str]) -> None:
    lines = [list(map(int, line.split())) for line in lines]
    #for line in lines:
    #print(is_safe_with_dampener(line), line)
    print(sum(map(is_safe_with_dampener, lines))) 

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
