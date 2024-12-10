from collections import defaultdict
from itertools import combinations
from enum import Enum
from sys import argv
class TileGroups(Enum):
    EMPTY = 1
    ANTENNA = 2
    ANTINODE = 3

    @staticmethod
    def from_symbol(symbol: str) -> "TileGroups":
        if symbol == '.':
            return TileGroups.EMPTY
        if symbol == '#':
            return TileGroups.ANTINODE
        if not symbol.isalnum():
            raise ValueError(f"Invalid symbol passed, cannot parse {symbol}")
        return TileGroups.ANTENNA

class Tile:
    board = None
    def __init__(self, y: int, x:int, symbol: str):
        self.symbol = symbol
        self.group = TileGroups.from_symbol(symbol)
        self.y = y
        self.x = x
    
        
def is_in_bounds(lines: list[str], y: int, x: int) -> bool:
    return 0 <= y < len(lines) and 0 <= x < len(lines[y])

def part1(lines: list[str]) -> int:
    antennae = defaultdict(list)
    for y, row in enumerate(lines):
        for x, letter in enumerate(row):
            if letter == '.':
                continue
            antennae[letter].append((y,x))
    antinodes = set()
    for point_list in antennae.values():
        for one, two in combinations(point_list, 2):
            first, second = min(one, two), max(one, two)
            dy, dx = second[0] - first[0], second[1] - first[1]
            #print(f"first: {first}, second: {second}, dy: {dy}, dx:{dx}")
            for y, x in [first, second]:
                y2, x2 = y-dy, x-dx
                if is_in_bounds(lines, y2, x2):
                    antinodes.add((y2, x2))
                dy, dx = -dy, -dx
    return len(antinodes) 


def emit(lines: list[str], p1: tuple[int, int], p2: tuple[int, int]) -> set[tuple[int, int]]:
    result = set()

    dy, dx = p2[0] - p1[0], p2[1] - p1[1]
    y, x = p1
    while is_in_bounds(lines, y, x):
        print(p1, p2, y,x)
        result.add((y,x))
        y += dy
        x += dx
    return result


def part2(lines: list[str]) -> int:
    antennae = defaultdict(list)
    for y, row in enumerate(lines):
        for x, letter in enumerate(row):
            if letter == '.' or letter == '#':
                continue
            antennae[letter].append((y,x))
    antinodes = set()
    print(antennae)
    for point_list in antennae.values():
        print(point_list)
        for one, two in combinations(point_list, 2):
            ray_one = emit(lines, one, two)
            ray_two = emit(lines, two, one)
            antinodes.update(ray_one)
            antinodes.update(ray_two)
    _lines = [list(line) for line in lines]
    for y, x in antinodes:
        if _lines[y][x] == '.':
            _lines[y][x] = '#'
    for line in _lines:
        print(''.join(line))
    
    return len(antinodes)


def main() -> None:
    path = "test.txt"
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        lines = [line.rstrip() for line in f if line] 
    one = part1(lines)
    print('part1:', one)
    two = part2(lines)
    print('part2:', two)


if __name__ == "__main__":
    main()
