'''
Exaple agent that does not do anything
'''
import time
import random

from . import agent_utils

class FreeRoamingAgent:
	def __init__(self):
		""" Example of an agent
		"""
		pass

	def next_move(self, game_state, player_state):
		""" This method is called each time the agent is required to choose an action
		"""

		# Lets pretend that agent is doing some thinking
		time.sleep(0.05)

		free_tiles = agent_utils.get_free_tiles(location=player_state.location, game_state=game_state)
		move = self.move_to_tile(player_state.location, random.choice(free_tiles)) if free_tiles else ''
		print(f"For tick {game_state.tick_number} I'm going to move: {move}")
		
		return move

	# given an adjacent tile location, move us there
	def move_to_tile(self, location, tile):
		if not tile: return ''

		# see where the tile is relative to our current location
		diff = tuple(y-x for x, y in zip(location, tile))

		# return the action that moves in the direction of the tile
		if   diff == ( 1, 0):	return 'r'
		elif diff == (-1, 0):	return 'l'
		elif diff == ( 0, 1):	return 'u'
		elif diff == ( 0,-1):	return 'd'
		else:					return ''
