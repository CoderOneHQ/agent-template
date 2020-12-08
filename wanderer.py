'''
This is a bot facing an existential crisis.
All it does is walk around the map.
'''

import time
import random

class agent:

	def __init__(self):
		pass

	def next_move(self, game_state, player_state):
		""" 
		This method is called each time the agent is required to choose an action
		"""

		########################
		###    VARIABLES     ###
		########################

		# list of all possible actions to take
		actions = ['', 'u', 'd', 'l','r','p']

		# store some information about the environment
		# game map is represented in the form (x,y)
		self.cols = game_state.size[0]
		self.rows = game_state.size[1]

		self.game_state = game_state # for us to refer to later

		self.location = player_state.location

		ammo = player_state.ammo

		bombs = game_state.bombs

		########################
		###      AGENT       ###
		########################

		# get our surrounding tiles
		surrounding_tiles = self.get_surrounding_tiles(self.location)

		# get list of empty tiles around us
		empty_tiles = self.get_empty_tiles(surrounding_tiles)

		# choose an empty tile to walk to
		random_tile = random.choice(empty_tiles)

		action = self.move_to_tile(self.location, random_tile)

		return action

	########################
	###     HELPERS      ###
	########################

	# given a tile location as an (x,y) tuple, this function
	# will return the surrounding tiles up, down, left and to the right as a list
	# (i.e. [(x1,y1), (x2,y2),...])
	# as long as they do not cross the edge of the map
	def get_surrounding_tiles(self, location):

		# find all the surrounding tiles relative to us
		# location[0] = col index; location[1] = row index
		tile_up = (location[0], location[1]+1)	
		tile_down = (location[0], location[1]-1)     
		tile_left = (location[0]-1, location[1]) 
		tile_right = (location[0]+1, location[1]) 		 

		# combine these into a list
		all_surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

		# we'll need to remove tiles that cross the border of the map
		# start with an empty list to store our valid surrounding tiles
		valid_surrounding_tiles = []

		# loop through our tiles
		for tile in all_surrounding_tiles:
			# check if the tile is within the boundaries of the game
			if self.game_state.is_in_bounds(tile):
				# if yes, then add them to our list
				valid_surrounding_tiles.append(tile)

		return valid_surrounding_tiles

	# given a list of tiles
	# return the ones which are actually empty
	def get_empty_tiles(self, tiles):

		# empty list to store our empty tiles
		empty_tiles = []

		for tile in tiles:
			if not self.game_state.is_occupied(tile):
				# the tile isn't occupied, so we'll add it to the list
				empty_tiles.append(tile)

		return empty_tiles

	# given an adjacent tile location, move us there
	def move_to_tile(self, location, tile):

		actions = ['', 'u', 'd', 'l','r','p']

		# see where the tile is relative to our current location
		diff = tuple(x-y for x, y in zip(self.location, tile))

		# return the action that moves in the direction of the tile
		if diff == (0,1):
			action = 'd'
		elif diff == (1,0):
			action = 'l'
		elif diff == (0,-1):
			action = 'u'
		elif diff == (-1,0):
			action = 'r'
		else:
			action = ''

		return action