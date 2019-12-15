"""
Classes, helper functions, and constants for 2048.
"""

import random
import copy

# Valid keyboard actions: note that these were the values
# I observed from using Python's input() function and the 
# arrow keys on a Macbook. There are likely more elegant
# solutions to reading keyboard input.
RIGHT = '\x1b[C'
LEFT = '\x1b[D'
DOWN = '\x1b[B'
UP = '\x1b[A'

# Valid game states.
WIN = "winning"
LOSE = "losing"
IN_PROGRESS = "in progress"

POSSIBLE_RANDOM_TILES = [2]*75 + [4]*25  # Hacky way to assign each value some occurrence probability.


class Tile:
    def __init__(self):
        self.curr_val = None
        self.merged_this_move = False

    def __str__(self):
        return str(self.curr_val) if self.curr_val != None else ' '
    
    def __repr__(self):
        return str(self)


class Board:
    def __init__(self, n=4):
        self.size = n
        self.grid = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        self.active_tiles = [] # list of Tile objects (by reference)
        self.inactive_tiles = [tile for row in self.grid for tile in row] 
        self.game_state = IN_PROGRESS

    def initialize_random_tile(self):
        if len(self.active_tiles) == pow(self.size, 2):
            return
        
        chosen_tile = random.choice(self.inactive_tiles)
        self.inactive_tiles.remove(chosen_tile)
        
        self.active_tiles.append(chosen_tile)
        chosen_tile.curr_val = random.choice(POSSIBLE_RANDOM_TILES)

    # Note that this function can be decomposed immensely more than I do here.
    def move(self, direction):
        """User enters LEFT, RIGHT, TOP, BOTTOM from keyboard."""
        # Move things to the specified direction as much as possible.
        # Only one thing can be merged in direction we head in. If we
        # are going in the direction RIGHT, then we prioritize the pairs
        # closest to the RIGHT side of row (WLOG for the other directions).
        if direction == RIGHT:
            for i in range(self.size):
                doubling = True  # True until we see the first doubling merge.
                anchor_tile = self.size - 2  # Can ignore shifting last tile in row,
                temp_tile = anchor_tile  # Will be modified as we shift and follow tile.
                while True:
                    if self.merge(self.grid[i][temp_tile], self.grid[i][temp_tile+1], doubling):
                        doubling = False
                    tile_moved = self.grid[i][temp_tile].curr_val is None
                    if tile_moved:
                        # Then try moving it again (it's now at next tile),
                        temp_tile += 1
                    if temp_tile >= self.size - 1 or not tile_moved:
                        # Done with this particular anchor tile, update next.
                        anchor_tile -= 1
                        temp_tile = anchor_tile
                            
                        if anchor_tile == -1:
                            break
        elif direction == LEFT:
            for i in range(self.size):
                doubling = True  
                anchor_tile = 0
                temp_tile = anchor_tile 
                while True:
                    if self.merge(self.grid[i][temp_tile+1], self.grid[i][temp_tile], doubling):
                        doubling = False
                    tile_moved = self.grid[i][temp_tile+1].curr_val is None
                    if tile_moved:
                        temp_tile -= 1
                    if temp_tile <= -1 or not tile_moved:
                        anchor_tile += 1
                        temp_tile = anchor_tile
                        if anchor_tile == self.size-1:
                            break
        elif direction == UP:
            for j in range(self.size):
                doubling = True 
                anchor_tile = 0
                temp_tile = anchor_tile 
                while True:
                    if self.merge(self.grid[temp_tile+1][j], self.grid[temp_tile][j], doubling):
                        doubling = False
                    tile_moved = self.grid[temp_tile+1][j].curr_val is None
                    if tile_moved:
                        temp_tile -= 1
                    if temp_tile <= -1 or not tile_moved:
                        anchor_tile += 1
                        temp_tile = anchor_tile
                        if anchor_tile == self.size-1:
                            break
        elif direction == DOWN:
            for j in range(self.size):
                doubling = True 
                anchor_tile = self.size - 2 
                temp_tile = anchor_tile 
                while True:
                    if self.merge(self.grid[temp_tile][j], self.grid[temp_tile+1][j], doubling):
                        doubling = False
                    tile_moved = self.grid[temp_tile][j].curr_val is None
                    if tile_moved:
                        temp_tile += 1
                    if temp_tile >= self.size - 1 or not tile_moved:
                        anchor_tile -= 1
                        temp_tile = anchor_tile
                        if anchor_tile == -1:
                            break
         
    def merge(self, first, second, doubling=True):
        """Attempts to merge this tile with another. This causes
        this tile's value to go back to None and the other tile's
        value doubles. Tiles must initially be the same curr_val
        in order to successfully merge. Alternatively, if the other
        tile is empty (curr_val = None), then we transfer curr_val
        to that tile. By default, we allow doubling, so 2 + 2 = 4,
        but we have the option to disable it since we should only
        merge two tiles along a row/col (depending on which direction
        the user inputted).
        
        Returns true iff the action was a doubling merge."""
        if doubling and first.curr_val == second.curr_val and first.curr_val != None:
            first.curr_val = None
            second.curr_val = second.curr_val * 2
            self.active_tiles.remove(first) 
            self.inactive_tiles.append(first)
            return True
        
        if first.curr_val != None and second.curr_val == None:
            second.curr_val = first.curr_val
            first.curr_val = None
            self.active_tiles.remove(first)
            self.inactive_tiles.append(first)
            self.inactive_tiles.remove(second)
            self.active_tiles.append(second)
        return False

    def get_tile_values(self):
        res = []
        for row in self.grid:
            for col in row:
                res.append(col.curr_val)
        return res

    def is_game_over(self):
        # A very lazy but sufficiently fast way to check for end state:
        #  -see if all directions yield the current board state.
        curr_tile_values = self.get_tile_values()

        if 2048 in curr_tile_values:
            self.game_state = WIN
            return True

        board_one = copy.deepcopy(self)
        board_two = copy.deepcopy(self)
        board_three = copy.deepcopy(self)
        board_four = copy.deepcopy(self)

        board_one.move(RIGHT)
        board_two.move(LEFT)
        board_four.move(DOWN)
        board_three.move(UP)

        board_one.initialize_random_tile()
        board_two.initialize_random_tile()
        board_three.initialize_random_tile()
        board_four.initialize_random_tile()

        if (board_one.get_tile_values() == curr_tile_values
            and board_two.get_tile_values() == curr_tile_values
            and board_three.get_tile_values() == curr_tile_values
            and board_four.get_tile_values() == curr_tile_values):

            self.game_state = LOSE
            return True

        return False

    def __str__(self):
        res = ''
        for row in self.grid:
            res += str(row) + '\n'
        return res

    def __repr__(self):
        return str(self)

