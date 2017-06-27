import sys
import math
from collections import namedtuple

Position = namedtuple('Position', 'y x')


# TODO: If there is a height 3 area opponent can reach first, build on it
# TODO: Avoid building on height 2 areas if opponent is adjacent to them
# TODO: Move back and forth between level 3 spots as much as possible,
# but build somewhere else
# TODO: Don't get stuck in a corner by opponent
# TODO: Don't build on your only move option from a square

# Can you build on a square occupied by an opponent?

def is_valid_square(board, move, other_pos):
    if (-1 in move or size in move or (move == other_pos) or
        board[move.y][move.x] in (".", "4")):
        # Position is off the grid, a hole, full, or occupied by opponent;
        #     cannot move or build in this direction
        return False
    return True

def is_valid_move(board, old_pos, new_pos, other_pos):
    if not is_valid_square(board, new_pos, other_pos):
        return False
    if int(board[old_pos.y][old_pos.x]) + 1 < (int(board[new_pos.y][new_pos.x])):
        # Cannot step up more than one level at a time
        return False
    return True

# Avoid duplicating this code to calculate new positions
def make_move(pos, direction):
    '''Given a position and direction, return the resulting position.'''
    dir_map = {"N": (-1, 0), "NE": (-1, 1), "E": (0, 1), "SE": (1, 1),
        "S": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)}
    return Position(pos.y + dir_map[direction][0], pos.x + dir_map[direction][1])

# Don't sort the resulting list because we can sort reversed or not depending on use
def find_adj(board, pos, other_pos):
    '''Returns a list of all directions with usable squares.
    Does not include directions leading to level 4 squares since they are not usable.

    Return format:
    [(height, direction), (height, direction) ...]
    '''
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    results = []
    for d in directions:
        new_pos = make_move(pos, d)
        if is_valid_square(board, new_pos, other_pos):
            results.append((int(board[new_pos.y][new_pos.x]), d))
    return results

# TODO: Don't move onto spots that have no <= 2 spots adjacent, UNLESS it is the end of the game
# Move to the best spot, then we will build on the best building spot from there
def find_best_move(board, unit_pos, other_pos):
    moves = sorted(find_adj(board, unit_pos, other_pos), reverse=True)
    # Choose the highest height square that has building options adjacent to it
    for height, d in moves:
        if find_adj(board, make_move(unit_pos, d), other_pos):
            return d

# Build on a now adjacent spot
def find_best_build(board, unit_pos, other_pos):
    moves = sorted(find_adj(board, unit_pos, other_pos), reverse=True)
    build_dir = "None"
    for height, d in moves:
        # Try to build on the highest < 3 level square we can, but if our only option
        #    is a level 3 square, build on one of those
        if height < 3:
            build_dir = d + " " + str(height)
            break
    else:
        new_pos = make_move(unit_pos, d)
        # Build on any of the level 3 squares (return direction of the first one)
        # The height should be 3 in this case
        build_dir = moves[0][1] + " " + board[new_pos.y][new_pos.x]
    return build_dir


size = int(raw_input())
units_per_player = int(raw_input())

# game loop
while True:
    board = []
    for _ in xrange(size):
        board.append(raw_input())
    for _ in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
        unit_pos = Position(unit_y, unit_x)
    for _ in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
        other_pos = Position(other_y, other_x)
    for _ in xrange(int(raw_input())):
        atype, index, dir_1, dir_2 = raw_input().split()
        index = int(index)
    move = find_best_move(board, unit_pos, other_pos)
    # Position changes after moving; build in best spot from that position
    build = find_best_build(board, make_move(unit_pos, move), other_pos)
    print "MOVE&BUILD 0 {} {}".format(move, build)
