
# given a tile location as an (x,y) tuple, this function
# will return the surrounding tiles up, down, left and to the right as a list
# (i.e. [(x1,y1), (x2,y2),...])
# as long as they do not cross the edge of the map
def get_free_tiles(location, game_state):

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
	return [tile for tile in all_surrounding_tiles if not game_state.entity_at(tile)]
