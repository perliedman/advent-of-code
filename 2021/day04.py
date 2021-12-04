# -*- coding: UTF-8
import sys

def play(number, boards):
    for number in numbers:
        to_remove = []
        for board in boards:
            for y in range(len(board)):
                for x in range(len(board[y])):
                    if board[y][x][0] == number:
                        board[y][x][1] = True

                        row_win = all([marked for (n, marked) in board[y]])
                        col_win = all([marked for (x, marked) in [row[x] for row in board]])
                        if row_win or col_win:
                            s = sum([x for row in board for (x, marked) in row if not marked])
                            yield (number, s, number * s)
                            to_remove.append(board)

        for board in to_remove:
            boards.remove(board)

def create_boards(lines):
    boards = []
    for start_line in range(2, len(lines), 6):
        board = [[[int(x), False] for x in l.strip().split()] for l in lines[start_line:start_line + 5]]
        boards.append(board)

    return boards

with open(sys.argv[1], 'r') as f:
    lines = f.readlines()

    numbers = [int(x) for x in lines[0].split(',')]

    wins = list(play(numbers, create_boards(lines)))
    print(wins[0][2], wins[-1][2])
