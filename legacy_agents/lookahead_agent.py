import time

class agent:
	def __init__(self, player_num, env):
		self.name = "lookahead bot"
		self.player_num = player_num
		self.env = env
		'''
		This might need to be added in future
				# This is the case if the player wants to decide on some actions before 
				#the start of the game
				self.board = solid_state["board"] 
				self.done = solid_state["done"]
				self.bombs = solid_state["bombs"]
				self.turn = solid_state["turn"]
				self.player = solid_state["players"][self.player_num-1]

		'''

	def give_next_move(self, solid_state):
		'''
		This method is called each time the player needs to choose an 
		action

		solid_state: is a dictionary containing all the information about the board
		''' 


		state = solid_state["board"] 
		done = solid_state["done"]
		bombs = solid_state["bombs"]
		turn = solid_state["turn"]
		player = solid_state["players"][self.player_num-1]

		BOARD_DICT = {'empty':0,'player1':1, 'player2':2,'soft_block':3,'hard_block':4,'bomb':5,'p1_on_bomb':6, 'p2_on_bomb':7, 'exploding_bomb':8, 'exploding_tile':9}
		ACTIONS_DICT = {0:(0,0),5:(0,0),1:(0,-1),2:(0,1),3:(-1,0),4:(1,0)}
		# dictionary for actions
		actions = ['none','left','right','up','down','bomb']
		action_id = [0,1,2,3,4,5]
		d_actions = dict(zip(actions,action_id))

		############################
		##### HELPER FUNCTIONS #####
		############################

		import random
		import os
		from time import sleep
		import numpy as np

		# get player reference id's for the map
		if player.number == 0:
			player_id = 1
			player_on_bomb_id = 6
		else:
			player_id = 2
			player_on_bomb_id = 7

		# get shape of the map
		rows = state.shape[0]
		cols = state.shape[1]
		inarow = 4 # number of tiles in a window

		# get bomb_timer
		if player.bombs:
			for bomb in player.bombs:
				bomb_timer=bomb.timer
		else:
			bomb_timer=5

		# calculates score if agent makes selected move
		def score_move(state, action, curr_pos, bomb_timer):
			next_state = make_move(state, action, curr_pos, bomb_timer)
			score = get_heuristic(next_state)
			#print(action)
			#print(next_state)
			#print(score)
			#sleep(5)
			return score

		# gets the state of the next map if agent makes selected move
		# agent doesn't know the bomb timer
		def make_move(state, action, curr_pos,bomb_timer):
			next_state = state.copy()
			new_pos = [sum(x) for x in zip(ACTIONS_DICT[action],curr_pos)]

			if action == d_actions['bomb']:
				next_state[tuple(new_pos)] = player_on_bomb_id
			elif action == d_actions['none']:
				pass
			else:
				next_state[tuple(new_pos)] = player_id

				if not next_state[curr_pos] == player_on_bomb_id:
					# clear previous position only if it wasn't a just-placed bomb
					next_state[curr_pos] = BOARD_DICT['empty']
				else:
					# player has left behind a bomb
					next_state[curr_pos] = BOARD_DICT['bomb']

			#print(bomb_timer)
			if bomb_timer == 1:
				next_state[bomb_pos] = BOARD_DICT['exploding_bomb']
			#### how to deal with staying on bomb
			#print(action)
			#print(next_state)
			return next_state

		def get_heuristic(state):
			# define configurations
			# GOOD CONFIGS
			g_config_1 = [BOARD_DICT['soft_block'], player_on_bomb_id, BOARD_DICT['empty'], BOARD_DICT['empty']]			# |  O  | P1* |     |     |
			g_config_2 = [BOARD_DICT['soft_block'], BOARD_DICT['soft_block'], player_on_bomb_id, BOARD_DICT['empty']]		# |  O  |  O  | P1* |     |
			g_config_3 = [BOARD_DICT['soft_block'], BOARD_DICT['soft_block'], BOARD_DICT['soft_block'], player_on_bomb_id]	# |  O  |  O  |  O  | P1* |
			g_config_4 = [BOARD_DICT['soft_block'], player_on_bomb_id, BOARD_DICT['empty'], BOARD_DICT['soft_block']]		# |  O  | P1* |     |  O  |
			g_config_5 = [BOARD_DICT['soft_block'], player_on_bomb_id, BOARD_DICT['soft_block'], BOARD_DICT['soft_block']]	# |  O  | P1* |  O  |  O  |
			g_config_6 = [BOARD_DICT['soft_block'], player_on_bomb_id, BOARD_DICT['soft_block'], BOARD_DICT['empty']]		# |  O  | P1* |  O  |     |
			g_config_7 = [BOARD_DICT['soft_block'], BOARD_DICT['bomb'], player_id, BOARD_DICT['empty']]						# |  O  |  *  | P1  |     |		
			g_config_8 = [BOARD_DICT['soft_block'], BOARD_DICT['bomb'], BOARD_DICT['empty'], player_id]						# |  O  |  *  |     | P1  |
			g_config_9 = [BOARD_DICT['soft_block'], BOARD_DICT['soft_block'], BOARD_DICT['bomb'], player_id]				# |  O  |  O  |  *  | P1  |		
			g_config_10 = [BOARD_DICT['soft_block'], BOARD_DICT['exploding_bomb'], BOARD_DICT['empty'], player_id]			# |  O  |  !  |     | P1  |		
			g_config_11 = [BOARD_DICT['exploding_bomb'], BOARD_DICT['empty'], BOARD_DICT['empty'], player_id]				# |  !  |     |     | P1  |		
			g_config_12 = [BOARD_DICT['empty'], player_id, BOARD_DICT['bomb'], BOARD_DICT['empty']]							# |     | P1  |  *  |     |		
			g_config_13 = [player_id, BOARD_DICT['empty'], BOARD_DICT['bomb'], BOARD_DICT['empty']]							# | P1  |     |  *  |     |		
			g_config_14 = [player_id, BOARD_DICT['empty'], BOARD_DICT['empty'], BOARD_DICT['bomb']]							# | P1  |     |     |  *  |		
			g_config_15 = [BOARD_DICT['empty'], player_id, BOARD_DICT['empty'], BOARD_DICT['bomb']]							# |     | P1  |     |  *  |		
			g_config_16 = [BOARD_DICT['empty'], BOARD_DICT['empty'], player_id, BOARD_DICT['bomb']]							# |     |     | P1  |  *  |		

			# BAD CONFIGS
			b_config_1 = [BOARD_DICT['empty'], BOARD_DICT['bomb'], player_id, BOARD_DICT['soft_block']]						# |     |  *  | P1  |  O  |
			b_config_2 = [BOARD_DICT['bomb'], player_id, BOARD_DICT['soft_block'], BOARD_DICT['soft_block']]				# |  *  |  P1 |  O  |  O  |
			b_config_3 = [BOARD_DICT['soft_block'], BOARD_DICT['bomb'], player_id, BOARD_DICT['soft_block']]				# |  O  |  *  | P1  |  O  |
			b_config_4 = [player_id, BOARD_DICT['exploding_bomb'], BOARD_DICT['empty'], BOARD_DICT['empty']]				# | P1  |  !  |     |     |
			b_config_5 = [player_id, BOARD_DICT['exploding_bomb'], BOARD_DICT['empty'], BOARD_DICT['soft_block']]			# | P1  |  !  |     |  O  |
			b_config_6 = [player_id, BOARD_DICT['exploding_bomb'], BOARD_DICT['soft_block'], BOARD_DICT['soft_block']]		# | P1  |  !  |  O  |  O  |
			b_config_7 = [player_id, BOARD_DICT['exploding_bomb'], BOARD_DICT['soft_block'], BOARD_DICT['empty']]			# | P1  |  !  |  O  |     |
			b_config_8 = [BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['empty'], BOARD_DICT['empty']]				# |  !  | P1  |     |     |
			b_config_9 = [BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['empty'], BOARD_DICT['soft_block']]			# |  !  | P1  |     |  O  |
			b_config_10 = [BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['soft_block'], BOARD_DICT['soft_block']]		# |  !  | P1  |  O  |  O  |
			b_config_11 = [BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['soft_block'], BOARD_DICT['empty']]			# |  !  | P1  |  O  |     |
			b_config_12 = [BOARD_DICT['empty'], BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['empty']]				# |     |  !  | P1  |     |
			b_config_13 = [BOARD_DICT['empty'], BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['soft_block']]			# |     |  !  | P1  |  O  |
			b_config_14 = [BOARD_DICT['soft_block'], BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['empty']]			# |  O  |  !  | P1  |     |
			b_config_15 = [BOARD_DICT['soft_block'], BOARD_DICT['exploding_bomb'], player_id, BOARD_DICT['soft_block']]		# |  O  |  !  | P1  |  O  |
			b_config_16 = [BOARD_DICT['bomb'], player_id, BOARD_DICT['soft_block'], BOARD_DICT['soft_block']]				# |  *  |  P1 |  O  |     |


			# list of configs
			list_configs = [g_config_1, g_config_2, g_config_3, g_config_4, g_config_5, g_config_6, g_config_7, g_config_8, g_config_9, g_config_10, g_config_11, 
			g_config_12, g_config_13, g_config_14,g_config_15, g_config_16,
			b_config_1, b_config_2, b_config_3, b_config_4, b_config_5, b_config_6, b_config_7, b_config_8, b_config_9, b_config_10, b_config_11, b_config_12, b_config_13, b_config_14, b_config_15, b_config_16]
			
			# Map points to configs
			rewards = [10, 10, 10, 10, 10, 10, 100, 1000, 100, 1000, 1000, 
			50, 500, 500, 500, 50,
			-10000, -10000, -10000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -100000, -10000]

			score = 0

			for config in list_configs:
				num_config = count_windows(state, config)
				score += num_config * rewards[list_configs.index(config)]
			#print(score)
			return score

		# checks if window satisfies heuristic conditions
		def check_window(window, config):
			#print(window)
			#print(config)
			#sleep(10)
			return (window == config or window == config[::-1])

		# counts number of windows satisfying heuristic conditions
		def count_windows(state,config):
			num_windows=0

			# HORIZONTAL
			for row in range(rows):
				for col in range(cols - inarow):
					window = list(state[row, col:(col+inarow)])
					if check_window(window,config):
						num_windows +=1

			# VERTICAL
			for col in range(cols):
				for row in range(rows - inarow):
					window = list(state[row:(row+inarow), col])
					if check_window(window,config):
						num_windows +=1

			return num_windows

		############################
		#####      AGENT       #####
		############################

		### find valid moves
		# get current location of agent
		curr_pos = np.where(state == player_id)
		if curr_pos[0].size==0 and curr_pos[1].size==0:
			# if player couldn't be found, check if the player is on a bomb
			curr_pos = np.where(state == player_on_bomb_id)

		# check if there is a bomb on the map
		bomb_pos = np.where(state == BOARD_DICT['bomb'])
		if bomb_pos[0].size==0 and bomb_pos[1].size==0:
			bomb_pos = np.where(state == BOARD_DICT['p1_on_bomb'])
		if bomb_pos[0].size==0 and bomb_pos[1].size==0:
			bomb_pos = np.where(state == BOARD_DICT['p2_on_bomb'])

		# get surrounding tiles
		tile_up = (curr_pos[0]-1,curr_pos[1])
		tile_down = (curr_pos[0]+1,curr_pos[1])
		tile_left = (curr_pos[0],curr_pos[1]-1)
		tile_right = (curr_pos[0],curr_pos[1]+1)

		surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

		# exclude tiles that cross the border of the board
		tiles_to_remove = []
		for tile in surrounding_tiles:
			if tile[0] < 0 or tile[1] < 0 or tile[0] >= rows or tile[1] >= cols:
				tiles_to_remove.append(tile)

		for tile in tiles_to_remove:
			surrounding_tiles.remove(tile)

		# find list of empty tiles
		empty_tiles = []
		for tile in surrounding_tiles:
			if state[tile] == 0:
				empty_tiles.append(tile)

		all_actions = [d_actions['up'],d_actions['down'],d_actions['left'],d_actions['right'],d_actions['none'],d_actions['bomb']]

		valid_actions = [d_actions['none']]
		# get valid moves
		for tile in empty_tiles:
			if tile == tile_up:
				valid_actions.append(d_actions['up'])
			elif tile == tile_down:
				valid_actions.append(d_actions['down'])
			elif tile == tile_left:
				valid_actions.append(d_actions['left'])
			elif tile == tile_right:
				valid_actions.append(d_actions['right'])

		valid_move_actions = valid_actions
		
		if bomb_pos[0].size==0 and bomb_pos[1].size==0:
			valid_actions.append(d_actions['bomb'])
			is_bomb = False
		else:
			is_bomb = True

		# calculate best next move
		scores = dict(zip(valid_actions, [score_move(state, action, curr_pos, bomb_timer) for action in valid_actions]))

		# Get a list of moves that maximize the heuristic
		max_actions = [key for key in scores.keys() if scores[key] == max(scores.values())]
		if max_actions:
			action = random.choice(max_actions)
		elif valid_move_actions:
			action = random.choice(valid_move_actions)
		else:
			action = random.choice(all_actions)

		return action


