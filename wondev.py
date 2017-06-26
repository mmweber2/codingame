# Code for the Wondev Woman challenge:
# https://www.codingame.com/ide/challenge/wondev-woman

# This code is still very early; it's currently in the Wood 3 league.

import sys
import math

def find_nearest_move(board, unit_x, unit_y):
    best_height = -1
    best_dir = "None"
    size = len(board)
    directions = {(-1, 0): "N", (-1, 1): "NE", (0, 1): "E",
        (1, 1): "SE", (1, 0): "S", (1, -1): "SW", (0, -1): "W", (-1, -1): "NW"}
    for dy, dx in directions:
        new_y = unit_y + dy
        new_x = unit_x + dx
        if -1 in (new_x, new_y) or size in (new_x, new_y) or board[new_y][new_x] == ".":
            # Cannot move or build in this direction
            continue
        if board[new_y][new_x] == "3":
            # Winning position; go there!
            best_dir = directions[(dy, dx)] + " " + directions[(0-dy, 0-dx)]
            break
        else:
            height = int(board[new_y][new_x])
            if height > best_height:
                best_height = height
                best_dir = directions[(dy, dx)] + " " + directions[(0-dy, 0-dx)]
            # TODO: Find a better position to build onto
    return best_dir

size = int(raw_input())
units_per_player = int(raw_input())
# Game loop
while True:
    board = []
    for _ in xrange(size):
        board.append(raw_input())
    for _ in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
    for _ in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
    for _ in xrange(int(raw_input())):
        atype, index, dir_1, dir_2 = raw_input().split()
    index = int(index)
    direc = find_nearest_move(board, unit_x, unit_y)
    print "MOVE&BUILD 0 {}".format(direc)
