from collections import defaultdict
from sys import argv


def parse_input(path: str) -> tuple:
    with open(path) as f:
        blob = f.read()
    rules_blob, run_blob = blob.split("\n\n")
    return rules_blob.split('\n'), run_blob.split('\n')


def parse_rules(rules_lines: list[str]) -> defaultdict[int, set[int]]:
    rules = defaultdict(set)
    for rule_line in rules_lines:
        before, after = (int(page) for page in rule_line.split('|'))
        rules[after].add(before)
    return rules


def parse_runs(runs_lines: list[str]) -> list[list[int]]:
    return [
            [int(page) for page in run.split(',')] for run in runs_lines if run.strip()
        ]


def check_run(rules: defaultdict[int, set[int]], run: list[int]) -> int:
    #print('##############################')
    #print('\n')
    #print('checking run', run)
    out_of_order = set()
    for to_print in run:
        #print('printing', to_print)
        if to_print in rules:
            #print(to_print, 'needs', rules[to_print])
            if to_print in out_of_order:
                #print(f'run failing on {to_print}, {rules[to_print]} not found')
                return 0
        #print(to_print,'success')
        out_of_order.update(rules[to_print]) 
    return run[len(run) // 2]


def part1(rules_lines: list[str], runs_lines: list[str]) -> int:
    rules, runs = parse_rules(rules_lines), parse_runs(runs_lines)
    #print(rules)
    return sum(check_run(rules, run) for run in runs)


def fix_run(rules: defaultdict[int, set[int]], run: list[int], start:int=0) -> int:
    #print('\n#############################')
    #print(f'fixing run {run}')
    #forbidden = dict()
    for i, page1 in enumerate(run[start:],start):
        #print(f'checking page {page1} at index {i}')
        forbidden = rules[page1]
        for j, page2 in enumerate(run[:i], ):
            if page2 in forbidden:
                #print(f'{(page1, i)} collision with page {page2} at index {j}')
                popped = run.pop(i)
                #print(f'after pop {run}')
                run.insert(max(0, j-1), popped)
                #print(f'new run is {run}')
                return 0
    #    forbidden.update(rules[page1])
    return run[len(run) // 2]


def part2(rules_lines: list[str], runs_lines: list[str]) -> int:
    rules, runs = parse_rules(rules_lines), parse_runs(runs_lines)
    rev_rules = defaultdict(set)
    for k,v in rules.items():
        for page in v:
            rev_rules[page].add(k)
    total = 0
    for run in runs:
        current = check_run(rules, run)
        if current:
            continue
        while not current:
            #print(rules)
            fix_run(rev_rules, run)
            current = check_run(rules, run)
        total += current
    return total


def main() -> None:
    path = "test.txt"
    if len(argv) == 2:
        path = argv[1]
    rules_lines, runs_lines = parse_input(path)
    one = part1(rules_lines, runs_lines)
    print('part1:', one) 
    two = part2(rules_lines, runs_lines)
    print('part2:', two)
    return


if __name__ == '__main__':
    main()
