'''
Doctor Strange (Monte Carlo Simulation class) AGENT
This agent uses the env object. env object is still under construction. Use it 
at your own risk.
Doctor Strange sees several possible futures. Then it takes the average of them to
choose the best move.
Since placing a bom can most likely causes in death so it does not do it.
It's simulation are all random.

It takes the average of the possible opponent moves
'''
import time

import random

class agent:
	def __init__(self, player_num, env):
		self.name = "doctor strange"
		self.player_num = player_num #player_num must always be deducted "player_num -1"
		self.env = env
		self.round_time = 3 # our agent things 3 second for each round



	def give_next_move(self, solid_state):
		'''
		This method is called each time the player needs to choose an 
		action

		solid_state: is a dictionary containing all the information about the board
		''' 

		
		self.board = solid_state["board"] 
		self.done = solid_state["done"]
		self.bombs = solid_state["bombs"]
		self.turn = solid_state["turn"]
		self.player = solid_state["players"][self.player_num-1]


		player1_moves, player2_moves =  self.env.get_valid_actions(solid_state)
		if ( self.player_num == 1):
			my_moves = player1_moves
			enemy_moves = player2_moves
		else:
			my_moves = player2_moves
			enemy_moves = player1_moves
		
		list_MC_nodes = []
		for mm in my_moves:
			list_future_states = [] # In this one, my moves are fixed
			for em in enemy_moves:
				if ( self.player_num == 1):
					joint_move = (mm, em)
				else:
					joint_move = (em, mm)
				list_future_states.append(self.env.next_state(solid_state,joint_move))
			list_MC_nodes.append(MC_node(list_future_states,mm))


		self.run_simulation(random.choice(list_MC_nodes).get_a_state())
		#TODO simulation works now just work with average

		timeout = time.time() + self.round_time   # 5 minutes from now
		counter = 0
		while time.time() < timeout:
			counter = counter + 1
			temp_MC_node = random.choice(list_MC_nodes)
			temp_reward = self.run_simulation(temp_MC_node.get_a_state())
			temp_MC_node.update_value(temp_reward)

		print("number of simulations: ", counter)

		#HERE we choose the best mc_node and so the best move
		optimal_mc = None
		highest_value = 0 # does not matter
		for mc_node in list_MC_nodes:
			if optimal_mc == None:
				optimal_mc = mc_node
				highest_value = mc_node.average_reward
			else:
				if (mc_node.average_reward > highest_value):
					optimal_mc = mc_node
					highest_value = mc_node.average_reward


		action = optimal_mc.action


		return action


	def run_simulation(self,solid_state):
		'''
		runs a random simulation until it reachs a terminal
		it then return the reward of the terminal
		'''
		temp_state = solid_state
		while(not temp_state["done"]):
			p1_m, p2_m =  self.env.get_valid_actions(temp_state)
			joint_move = (random.choice(p1_m),random.choice(p2_m))
			temp_state = self.env.next_state(temp_state,joint_move)
			#print("-> joint move: ", joint_move, " <-")
		#now temp_state is a terminal
	
		return temp_state["players"][self.player_num-1].score #might need to make it to work for all players


		#player1_moves, player2_moves =  self.env.get_valid_actions(solid_state)

class MC_node:
	def __init__(self, state_list, action):
		'''
		MC_node holds the first initial nodes of a next step
		'''
		self.state_list = state_list
		self.action = action # this is the action of us of
		self.average_reward = 0
		self.probability_of_states = {}
		#for s in state_list:
		#	self.probability_of_states[s]= 0# this checks the higher probability move

	def get_a_state(self):
		'''
		This method needs to be changed so it returns with probability 
		'''
		return random.choice(self.state_list)


	def update_value(self, new_result):
		self.average_reward = self.average_reward + new_result






