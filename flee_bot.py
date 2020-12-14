'''
This is a flee bot.
It places bombs and runs away. As a flee bot should.
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

		# for us to refer to later
		self.game_state = game_state 
		self.location = player_state.location

		ammo = player_state.ammo

		bombs = game_state.bombs

		########################
		###      AGENT       ###
		########################

		# first, check if we're within range of a bomb
		# get list of bombs within range
		bombs_in_range = self.get_bombs_in_range(self.location, bombs)

		# get our surrounding tiles
		surrounding_tiles = self.get_surrounding_tiles(self.location)

		# get list of empty tiles around us
		empty_tiles = self.get_empty_tiles(surrounding_tiles)

		# if I'm on a bomb, I should probably move
		if game_state.entity_at(self.location) == 'b':

			#print("I'm on a bomb. I'm going to move.")

			if empty_tiles:
				# choose a random free tile to move to
				random_tile = random.choice(empty_tiles)
				action = self.move_to_tile(self.location, random_tile)
			else:
				# if there isn't a free spot to move to, we're probably stuck here
				action = ''

		# if we're near a bomb, we should also probably move
		elif bombs_in_range:

			#print("I'm fleeing.")

			if empty_tiles:

				# get the safest tile for us to move to
				safest_tile = self.get_safest_tile(empty_tiles, bombs_in_range)	

				action = self.move_to_tile(self.location, safest_tile)

			else:
				action = random.choice(actions)	

		# if there are no bombs in range
		else:

			#print("I'm placing a bomb")

			# but first, let's check if we have any ammo
			if ammo > 0:
				# we've got ammo, let's place a bomb
				action = 'p'
			else:
				# no ammo, we'll make random moves until we have ammo
				action = random.choice(actions)	

		return action

	########################
	###     HELPERS      ###
	########################

	# returns the manhattan distance between two tiles, calculated as:
	# 	|x1 - x2| + |y1 - y2|
	def manhattan_distance(self, start, end):

		distance = abs(start[0] - end[0]) + abs(start[1] - end[1])

		return distance

	# given a location as an (x,y) tuple and the bombs on the map
	# we'll return a list of the bomb positions that are nearby
	def get_bombs_in_range(self, location, bombs):

		# empty list to store our bombs that are in range of us
		bombs_in_range = []

		# loop through all the bombs placed in the game
		for bomb in bombs:

			# get manhattan distance to a bomb
			distance = self.manhattan_distance(location, bomb)

			# set to some arbitrarily high distance
			if distance <= 10:
				bombs_in_range.append(bomb)

		return bombs_in_range

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

	# given a list of tiles and bombs
	# find the tile that's safest to move to
	def get_safest_tile(self, tiles, bombs):

		# which bomb is closest to us?
		bomb_distance = 10  # some arbitrary high distance
		closest_bomb = bombs[0]

		for bomb in bombs:
			new_bomb_distance = self.manhattan_distance(bomb,self.location)
			if new_bomb_distance < bomb_distance:
				bomb_distance = new_bomb_distance
				closest_bomb = bomb

		safe_dict = {}
		# now we'll figure out which tile is furthest away from that bomb
		for tile in tiles:
			# get the manhattan distance
			distance = self.manhattan_distance(closest_bomb, tile)
			# store this in a dictionary
			safe_dict[tile] = distance

		# return the tile with the furthest distance from any bomb
		safest_tile = max(safe_dict, key=safe_dict.get)

		return safest_tile

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