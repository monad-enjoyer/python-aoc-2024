from enum import Enum
from sys import argv

class Directions(Enum):
    NORTH = (-1, 0)
    NORTHEAST = (-1, 1)
    EAST = (0, 1)
    SOUTHEAST = (1, 1)
    SOUTH = (1, 0)
    SOUTHWEST = (1, -1)
    WEST = (0, -1)
    NORTHWEST = (-1, -1)


def is_valid_coord(board: list[list[str]], y: int, x: int) -> bool:
    return 0 <= y < len(board) and 0 <= x < len(board[y])


def search_directon(board: list[list[str]], y: int, x: int, heading: Directions) -> int:
    dy, dx = heading.value
    for i in range(1,4):
        y += dy
        x += dx
        if not is_valid_coord(board, y, x):
            return 0
        if board[y][x] != 'XMAS'[i]:
            return 0
    return 1

        
def part1(board: list[list[str]]) -> int:
    found = 0
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == 'X':
                found += sum(map(lambda direction: search_directon(board, y, x, direction), Directions))
    return found


    #def diagnol_search(board[list[list[str]]], y: int, x: int, heading):
    #if 

def search_cross(board: list[list[str]], y: int, x: int, cross:Directions) -> int:
    acceptable = [["M", "S"],
                  ["S", "M"]]
    check =[False, False]
    dy, dx = cross.value
    y1, x1 = y + dy, x + dx
    y2, x2 = y - dy, x - dx
    if is_valid_coord(board, y1, x1) and is_valid_coord(board, y2, x2):
        #print(f"{(y1, x1)},  {(y2, x2)}, {board[y][x]}, {board[y1][x1]}, {board[y2][x2]}")
        if [board[y1][x1], board[y2][x2]] in acceptable:
            return True
    return False



def part2(board: list[list[str]]) -> int:
    found = 0
    diagnols = [Directions.NORTHEAST, Directions.SOUTHEAST]
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == 'A':
                found += 1 if search_cross(board, y, x, diagnols[0]) and search_cross(board, y, x, diagnols[1]) else 0
    return found

def main() -> None:
    path = 'test.txt'
    if len(argv) == 2:
        path = argv[1]
    with open(path) as f:
        board = [list(line.strip()) for line in f.readlines() if line.strip()]
    one = part1(board)
    print(one)
    two = part2(board)
    print(two)



if __name__ == "__main__":
    main()
