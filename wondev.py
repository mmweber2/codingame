import sys
import math
from collections import namedtuple

Unit = namedtuple('Unit', 'id ally y x')

# TODO: If there is a height 3 area opponent can reach first, build on it
# TODO: Avoid building on height 2 areas if opponent is adjacent to them
# TODO: Move back and forth between level 3 spots as much as possible,
# but build somewhere else
# TODO: Don't get stuck in a corner by opponent
# TODO: Try pushing opponent

# Can you build on a square occupied by an opponent?

def is_valid_square(board, pos, other_units):
    '''Returns True if the square at pos is a valid position.

    A valid position is on the grid and does not contain a hole,
        level 4 building, or another unit.
    '''
    for unit in other_units:
        if unit.x == pos[1] and unit_y == pos[0]:
            return False
    if (-1 in pos or size in pos or board[pos[0]][pos[1]] in (".", "4")):
        return False
    return True

def is_valid_move(board, unit, new_pos, other_units):
    '''Returns True if unit can move to position new_pos.

    new_pos must be a valid square to move or build onto, and the
        difference in height between the unit's current position
        and new_pos must not be greater than 1, but may be negative.

    Can be used for either allied or enemy units.
    '''
    if not is_valid_square(board, new_pos, other_units):
        return False
    if int(board[unit.y][unit.x]) + 1 < (int(board[new_pos[0]][new_pos[1]])):
        # Cannot step up more than one level at a time
        return False
    return True

# Avoid duplicating this code to calculate new positions
def make_move(unit, direction):
    '''Given a position and direction, return the resulting position.

    This function does not change the location of the unit, only
    calculates its new position.
    '''
    dir_map = {"N": (-1, 0), "NE": (-1, 1), "E": (0, 1), "SE": (1, 1),
        "S": (1, 0), "SW": (1, -1), "W": (0, -1), "NW": (-1, -1)}
    return (unit.y + dir_map[direction][0], unit.x + dir_map[direction][1])

def find_adj(board, unit, other_units):
    '''Returns a sorted list of all directions with usable squares.

    Does not include directions leading to level 4 squares since they are not usable.
    The list is returned in decreasing order of height.

    Return format:
    [(height, direction), (height, direction) ...]
    '''
    # TODO: Implement pushing
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    results = []
    for d in directions:
        new_y, new_x = make_move(unit, d)
        if is_valid_square(board, (new_y, new_x), other_units):
            results.append((int(board[new_y][new_x]), d))
    return sorted(results, reverse=True)

# Move to the best spot, then we will build on the best building spot from there
# TODO: Implement pushing
def find_best_move(board, unit, other_units):
    moves = find_adj(board, unit, other_units)
    # TODO: Might be possible to move into a dead end position as a last move,
    # that could get an additional point per unit.
    # Choose the highest height square that has building options adjacent to it
    for height, d in moves:
        new_pos = make_move(unit, d)
        if not is_valid_move(board, unit, new_pos, other_units):
            continue
        # find_adj requires a unit, so make a dummy unit to test moves
        # Make sure there are other moves from this position
        # (Don't move into a dead end)
        if len(find_adj(board, Unit(-1, True, new_pos[0], new_pos[1]), other_units)) > 0:
            return d

# Build on a now adjacent spot
# Other is now a list of other units' positions
# Since we already have the unit from when we chose the move, this function
#     will only search for one of the units.
# This function doesn't need to treat enemy units differently, because
#     it will only be run for MOVE&BUILD commands.
# TODO: Can we build on top of other units? Currently this code allows it.
def find_best_build(board, unit, other_units):
    moves = find_adj(board, unit, other_units)
    build_dir = "None"
    # Moves only has 2 items because we did not include the unit/id
    for height, d in moves:
        # Try to build on the highest < 3 level square we can, but if our only option
        #    is a level 3 square, build on one of those
        if height < 3:
            assert height == 3
            build_dir = d + " " + "3"
            break
    else:
        if d == "None":
            print "Could not build from ", unit.y, unit.x
        new_y, new_x = make_move(unit, d)
        # Build on any of the level 3 squares (return direction of the first one)
        # The height should be 3 in this case
        assert board[new_y][new_x] == "3"
        build_dir = moves[0][1] + " " + "3"
    return build_dir


size = int(raw_input())
units_per_player = int(raw_input())

# game loop
while True:
    board = []
    for _ in xrange(size):
        board.append(raw_input())
    units = []
    for i in xrange(units_per_player):
        unit_x, unit_y = [int(j) for j in raw_input().split()]
        units.append(Unit(i, True, unit_y, unit_x))
    for i in xrange(units_per_player):
        other_x, other_y = [int(j) for j in raw_input().split()]
        units.append(Unit(i + units_per_player, False, other_y, other_x))
    for _ in xrange(int(raw_input())):
        atype, index, dir_1, dir_2 = raw_input().split()
        index = int(index)
    # TODO: Assign a score to the move for each unit and choose best one
    # Since allied units are provided first, the first half
    #     of the list will be the allied units
    moves = []
    for unit_id in xrange(len(units) / 2):
        print >> sys.stderr, "unit id is ", unit_id
        curr_unit = units[unit_id]
        assert curr_unit.ally
        other_units = units[:curr_unit.id] + units[curr_unit.id+1:]
        moves.append((unit_id, find_best_move(board, curr_unit, other_units)))
    # TODO: Find a better way to decide which unit to use
    unit, move = sorted(moves)[0]
    # TODO: Add check to see if this involves a push
    #print "PUSH&BUILD {} {} {}".format(unit_id, "X", "X")
    # TODO: Explore pushing separately since it doesn't require build searching
    # Position changes after moving; build in best spot from that position
    other_units = units[:curr_unit.id] + units[curr_unit.id+1:]
    # Remake unit since it has made the move (tuple is immutable)
    new_y, new_x = make_move(units[unit], move)
    moved_unit = Unit(unit.id, True, new_y, new_x)
    # TODO: Implement pushing and building based on unit
    build = find_best_build(board, moved_unit, other_units)
    print "MOVE&BUILD {} {} {}".format(unit, move, build)
