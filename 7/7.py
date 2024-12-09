from dataclasses import dataclass
from functools import reduce
from math import floor, log10
from sys import argv

class Line:
    def __init__(self, line: str):
        fields = line.strip().split(':')
        self.target = int(fields[0])
        self.operands = tuple(int(num) for num in fields[1].split())

    def is_target_reachable(self, should_or=False) -> int:
        working = {self.operands[0],}
        to_add = []
        for operand in self.operands[1:]:
            power = 10 ** (floor(log10(operand)) + 1)
            to_add.append({num + operand for num in working})
            to_add.append({num * operand for num in working})
            if should_or:
                to_add.append({num * power + operand for num in working})
            #print(working)
            working = reduce(lambda first, second: first.union(second), to_add)
            #if self.target in working:
            #print(working)
            #print(self)
        return self.target if self.target in working else 0
    

    def backtrack(self, i: int, working: set, should_or:bool=False) -> bool:
        if i == 0:
            return self.backtrack(1, {self.operands[0],}, should_or)
        if i == len(self.operands):
            return self.target in working
        if self.backtrack(i+1, {num + self.operands[i] for num in working},should_or) or self.backtrack(i+1, {num * self.operands[i] for num in working}, should_or):
            return True
        if not should_or:
            return False
        power = 10 ** (floor(log10(self.operands[i])) + 1)
        return self.backtrack(i +1, {num * power + self.operands[i] for num in working}, should_or)
        
        
        
    def __repr__(self):
        return f"{self.target}: {' '.join((str(num) for num in self.operands))}"
    
def part1(lines: list[Line]):
    #return sum(line.is_target_reachable() for line in lines)
    return sum(map(lambda line: line.target if line.backtrack(0, set()) else 0, lines))
def part2(lines: list[Line]):
    return sum(map(lambda line: line.target if line.backtrack(0, set(),True) else 0, lines))

def main() -> None:
    path = 'test.txt'
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        lines = [Line(line) for line in f if line.strip()]
    one = part1(lines)
    print(one)
    two = part2(lines)
    print(two)
if __name__ == "__main__":
    main()
