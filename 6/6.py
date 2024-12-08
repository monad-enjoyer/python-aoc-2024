from copy import deepcopy
from enum import Enum
from sys import argv
from typing import Optional




class Tile(Enum):
    EMPTY = '.'
    BLOCKED = '#'
    GUARD = '^'
    WALKED = '@'
    
    @staticmethod
    def from_char(char: str) -> Optional["Tile"] :
        match char:
            case '.':
                return Tile.EMPTY
            case '#':
                return Tile.BLOCKED
            case '^':
                return Tile.GUARD
            case '@':
                return Tile.WALKED
            case _:
                return None
    

def find_guard(lines: list[list[Tile|None]]) -> tuple[int, int]:
    for y, row in enumerate(lines):
        for x, letter in enumerate(row):
            if letter == Tile.GUARD:
                return y, x
    raise ValueError("Cannot find guard character '^' in input")


class GuardState(Enum):
    WALKING = 1
    OUT_OF_BOUNDS = 2
    CYCLE_DETECTED = 3

class Heading(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    @staticmethod
    def from_deltas(dy:int, dx: int) -> "Heading":
        to_find = (dy, dx)
        for direction in Heading:
            if to_find == direction.value:
                return direction
        raise ValueError(dy, dx, "is not a valid Heading")
        

class Guard():
    
    def __init__(self, board:list[list[Tile|None]], y=None, x=None, dy=-1, dx=0, has_walked:set[tuple[int, int, Heading]]=set()):
        self.board = board
        if y is not None and x is not None:
            self.y = y
            self.x = x
        else:
            self.y, self.x = find_guard(board)
        self.dy = dy
        self.dx = dx
        self.has_walked = set()
    
    def is_in_bounds(self, y: Optional[int]=None, x: Optional[int]=None) -> bool:
        if y is None:
            y = self.y
        if x is None:
            x = self.x
        return 0 <= y < len(self.board) and 0 <= x < len(self.board[self.y])
    
    def turn_right(self) -> None:
        self.dy, self.dx = self.dx, -self.dy

    def get_state(self) -> tuple[int, int, Heading]:
        return self.y, self.x, Heading.from_deltas(self.dy, self.dx)

    def take_turn(self) -> GuardState:
        if not self.is_in_bounds():
            return GuardState.OUT_OF_BOUNDS
        state = self.get_state()
        if state in self.has_walked:
            return GuardState.CYCLE_DETECTED
        self.has_walked.add(state)
        self.board[self.y][self.x] = Tile.WALKED
        y2, x2 = self.y + self.dy, self.x + self.dx
        if not self.is_in_bounds(y=y2, x=x2):
            return GuardState.OUT_OF_BOUNDS
        if self.board[y2][x2] is Tile.BLOCKED:
            self.turn_right()
        else:
            self.y, self.x = y2, x2
        return GuardState.WALKING


def part1(lines: list[list[Tile|None]]) -> int:
    y0, x0 = find_guard(lines)
    guard = Guard(lines, y0, x0)
    #lines[6][3] = Tile.BLOCKED
    check = GuardState.WALKING
    while check is GuardState.WALKING:
        check = guard.take_turn()
    print(check)
    for line in guard.board:
        print(''.join(x.value for x in line))
    return sum(map( lambda line: line.count(Tile.WALKED), lines))


def find_path(lines: list[list[Tile|None]]) -> list[tuple[int, int]]:
    y0, x0 = find_guard(lines)
    guard = Guard(lines, y0, x0)
    check = GuardState.WALKING
    while check is GuardState.WALKING:
        check = guard.take_turn()
    #return [t for t in zip(range(len(guard.board)), range(len(guard.board[0]))) if guard.board[t[0]][t[1]] is Tile.WALKED and t != (y0,x0)]
    result = []
    for y, row in enumerate(guard.board):
        for x, tile in enumerate(row):
            if tile is Tile.WALKED and (y,x) != (y0, x0):
                result.append((y,x))
    return result

def part2(lines: list[list[Tile|None]]) -> int:
    total = 0
    possible = find_path(deepcopy(lines))
    for y,x in possible:
        fresh = deepcopy(lines)
        fresh[y][x] = Tile.BLOCKED
        y0, x0 = find_guard(fresh)
        guard = Guard(fresh, y= y0, x=x0)
        check = GuardState.WALKING
        while check is GuardState.WALKING:
            check = guard.take_turn()
        if check == GuardState.CYCLE_DETECTED:
            total += 1
    return total
            



def main() -> None:
    path = 'test.txt'
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        lines = [[Tile.from_char(letter)for letter in line.strip()] for line in f if line.strip()]
    one = part1(deepcopy(lines))
    print(one)
    two = part2(deepcopy(lines))
    print(two)


if __name__ == '__main__':
    main()
