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
# TODO: Now have two units, choose one of them to move
# TODO: Try pushing opponent

# Can you build on a square occupied by an opponent?

# TODO: Update to allow pushing
# Other pos is now a list of Positions
def is_valid_square(board, move, other_pos):
    '''Returns True if the square at move is a valid position.
    
    A valid position is on the grid and does not contain a hole,
        level 4 building, or another unit.
    '''
    if (-1 in move or size in move or (move in other_pos) or
        board[move.y][move.x] in (".", "4")):
        return False
    return True
    
def is_valid_move(board, old_pos, new_pos, other_pos):
    '''Returns True if the change from old_pos to new_pos is valid.
    
    new_pos must be a valid square to move or build onto, and the
        difference in height between old_pos and new_pos must not
        be greater than 1, but may be negative.
    '''
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

def find_adj(board, pos, other_pos):
    '''Returns a sorted list of all directions with usable squares.
    
    Does not include directions leading to level 4 squares since they are not usable.
    The list is returned in decreasing order of height.
    
    Return format:
    [(height, direction), (height, direction) ...] 
    '''
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    results = []
    for d in directions:
        new_pos = make_move(pos, d)
        if is_valid_square(board, new_pos, other_pos):
            results.append((int(board[new_pos.y][new_pos.x]), d))
    return sorted(results, reverse=True)
    
# TODO: Don't move onto spots that have no <= 2 spots adjacent, UNLESS it is the end of the game
# Move to the best spot, then we will build on the best building spot from there
def find_best_move(board, my_units, other_pos):
    moves = []
    for i in xrange(len(my_units)):
        # Count my other unit as an 'other' unit
        # TODO: Enable pushing
        other = other_pos.append(my_units[1-i])
        moves.extend(move + (i,) for move in find_adj(board, my_units[i], other))
    # Choose the highest height square that has building options adjacent to it
    for height, d, unit in moves:
        unit_pos = my_units[unit]
        other = other_pos.append(my_units[1-unit])
        if not is_valid_move(board, unit_pos, make_move(unit_pos, d), other):
            continue
        if len(find_adj(board, make_move(unit_pos, d), other)) > 1:
            return (d, unit)
            
# Build on a now adjacent spot
# Other is now a list of other positions
# Since we already have the unit from when we chose the move, this function
#     will only search for one of the units.
# TODO: Can we build on top of our other unit? Currently code allows it.
def find_best_build(board, unit_pos, other_pos):
    moves = find_adj(board, unit_pos, other_pos)
    build_dir = "None"
    for height, d, unit in moves:
        # Try to build on the highest < 3 level square we can, but if our only option
        #    is a level 3 square, build on one of those
        if height < 3:
            build_dir = d + " " + str(height)
            break
    else:
        if d == "None":
            print "Could not build from ", unit_pos
        new_pos = make_move(unit_pos, d)
        # Build on any of the level 3 squares (return direction of the first one)
        # The height should be 3 in this case
        assert board[new_pos.y][new_pos.x] == 3
        build_dir = moves[0][1] + " " + 3
    return build_dir
                
        
size = int(raw_input())
units_per_player = int(raw_input())

# game loop
while True:
    board = []
    for _ in xrange(size):
        board.append(raw_input())
    my_units = []
    enemy_units = []
    for _ in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
        my_units.append(Position(unit_y, unit_x))
    for _ in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
        enemy_units.append(Position(other_y, other_x))
    for _ in xrange(int(raw_input())):
        atype, index, dir_1, dir_2 = raw_input().split()
        index = int(index)
    # TODO: Find a better way to decide which unit?
    # TODO: Assign a score to the move for each unit and choose best one
    move, unit = find_best_move(board, my_units, enemy_units)
    # Position changes after moving; build in best spot from that position
    build = find_best_build(board, make_move(my_units[unit], move), enemy_units)
    print "MOVE&BUILD {} {} {}".format(unit, move, build)