# Code for the Wondev Woman challenge:
# https://www.codingame.com/ide/challenge/wondev-woman

# This code is still very early; it's currently in the Wood 2 league.

import sys
import math

# TODO: If there is a height 3 area opponent can reach first, build on it
# TODO: Avoid building on height 2 areas if opponent is adjacent to them
# TODO: Don't ever jump off a level 2 or 3 pos onto the ground!
# TODO: Move back and forth between level 3 spots as much as possible,
# but build somewhere else
# Don't build on level 3 spots if the opponent is not close
# Don't get stuck in a corner by opponent

# Can you build on a square occupied by an opponent?

def is_valid_square(board, move, other_pos):
    '''Returns True if this square can be moved to or built on.'''
    new_y, new_x = move
    other_y, other_x = other_pos
    if (-1 in move or size in move or (new_y == other_y and new_x == other_x) or
        board[new_y][new_x] in (".", "4")):
        # Position is off the grid, a hole, full, or occupied by opponent;
        #     cannot move or build in this direction
        return False
    return True

def is_valid_move(board, old_pos, new_pos, other_pos):
    '''Returns True if the move is possible from the current position.'''
    if not is_valid_square(board, new_pos, other_pos):
        return False
    old_y, old_x = old_pos
    new_y, new_x = new_pos
    if int(board[old_y][old_x]) < int(board[new_y][new_x]) + 1:
        # Cannot step up more than one level at a time
        return False
    return True

# Since building comes after moving, we can build in the best spot within a 5 x 5
#     grid - the furthest we can move is two in any diagonal direction.
# Find the best spot to build, then move toward it and build.
def find_best_build(board, unit_x, unit_y, other_x, other_y):
    best_height = -1
    best_dir = "None"
    size = len(board)
    # All possible positions and the directions they can be built on from
    two_move_map = {
        (-2, -2): "NW", (-2, -1): "N NW", (-2, 0): "N NE NW", (-2, 1): "NE N",
        (-2, 2): "NE", (-1, -2): "NW W", (-1, -1): "N W", (-1, 0): "NE NW",
        (-1, 1): "N E", (-1, 2): "NE E", (0, -2): "NW W SW", (0, -1): "NW SW",
        (0, 0): "N NE E SE S SW W NW", (0, 1): "NE SE", (0, 2): "E NE SE",
        (1, -2): "SW W", (1, -1): "S W", (1, 0): "SE SW", (1, 1): "S E",
        (1, 2): "E SE", (2, -2): "SW", (2, -1): "S SW", (2, 0): "S SE SW",
        (2, 1): "S SE", (2, 2): "SE"]}
    direction_map = {"N": (-1, 0), "NE": (-1, 1), "E": (0, 1), "SE": (1, 1),
        "S": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)}
    for dy, dx in move_map:
        new_y = unit_y + dy
        new_x = unit_x + dx
        # Must verify that both the building position and the move position are valid
        # First, check building position
        if not is_valid_move(board, (unit_y, unit_x), (new_y, new_x), (other_y, other_x)):
            continue
        # Most building positions have multiple move positions, so find any valid one
        # TODO: Find the best one, not just any
        for d in move_map[(dy, dx)].split():
            move_y, move_x = direction_map[d]
            if not is_valid_move(board, (unit_y, unit_x), (move_y, move_x), (other_y, other_x)):
                # Cannot build from this position; try another one if possible
                continue
            # TODO: Pick up here
            if board[new_y][new_x] == "3":
                # Winning position; go there!
                best_dir = d + " " + directions[(0-dy, 0-dx)]
                break
         else:
             height = int(board[new_y][new_x])
             if height > best_height:
                 best_height = height
                 best_dir = directions[(dy, dx)] + " " + directions[(0-dy, 0-dx)] + " " + str(best_height)

# 5 <= size <= 7
size = int(raw_input())
 # Always 1 in the current league
units_per_player = int(raw_input())

# Game loop
while True:
    board = []
    for _ in xrange(size):
        board.append(raw_input())
    # Only 1 in the current league
    for _ in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
    # Cannot move onto this square
    for _ in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
    # This seems to include invalid input, so I'm not sure what it's for
    for _ in xrange(int(raw_input())):
        atype, index, dir_1, dir_2 = raw_input().split()
    index = int(index)
    direc = find_nearest_move(board, unit_x, unit_y)
    print "MOVE&BUILD 0 {}".format(direc)
