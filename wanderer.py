'''
Just a simple wandering agent
'''

import random

class Agent:

    def __init__(self):
        '''
        Place any initialization code for your agent here (if any)
        '''
        pass

    def next_move(self, game_state, player_state):
        '''
        This method is called each time your Agent is required to choose an action
        '''

        ########################
        ###    VARIABLES     ###
        ########################

        # get information about the map size
        self.cols = game_state.size[0]
        self.rows = game_state.size[1]

        # useful for later
        self.game_state = game_state 
        self.location = player_state.location

        ########################
        ###      AGENT       ###
        ########################

        # get our surrounding tiles
        surrounding_tiles = self.get_surrounding_tiles(self.location)

        # get list of empty tiles around us
        empty_tiles = self.get_empty_tiles(surrounding_tiles) 

        if empty_tiles:
            # choose an empty tile to walk to
            random_tile = random.choice(empty_tiles)
            action = self.move_to_tile(self.location, random_tile) 
    
        else:
            # we're trapped
            action = ''

        return action

    ########################
    ###      HELPERS     ###
    ########################
    
    # given our current location as an (x,y) tuple, return the surrounding tiles as a list
    # (i.e. [(x1,y1), (x2,y2),...])
    def get_surrounding_tiles(self, location):

        # location[0] = x-index; location[1] = y-index
        tile_north = (location[0], location[1]+1)	
        tile_south = (location[0], location[1]-1)
        tile_west = (location[0]-1, location[1])
        tile_east = (location[0]+1, location[1]) 		 
    
        surrounding_tiles = [tile_north, tile_south, tile_west, tile_east]
    
        for tile in surrounding_tiles:
            # check if the tile is within the boundaries of the game
            if not self.game_state.is_in_bounds(tile):
                # remove invalid tiles from our list
                surrounding_tiles.remove(tile)

        return surrounding_tiles
    
    # given a list of tiles, return only those that are empty/free
    def get_empty_tiles(self, tiles):

        empty_tiles = []

        for tile in tiles:
            if not self.game_state.is_occupied(tile):
                # add empty tiles to list
                empty_tiles.append(tile)

        return empty_tiles
        
    # given an adjacent tile location, move us there
    def move_to_tile(self, location, tile):

        # see where the tile is relative to our current location
        diff = tuple(x-y for x, y in zip(tile, self.location))

        # return the action that moves in the direction of the tile
        if diff == (0,1):
            action = 'u'
        elif diff == (0,-1):
            action = 'd'
        elif diff == (1,0):
            action = 'r'
        elif diff == (-1,0):
            action = 'l'
        else:
            action = ''

        return action
