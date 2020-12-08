'''
Smart Tree Class AGENT
What this agent does, is:
1. Looks for a block to explode
2. Finds the path toward that block
3. When reached, places a expl
4. Runs away from it
5. Waits till it explodes
6. Repeats

This is a good example if you want to use simple board search in 
your agent. It uses the search twice. Once to find a block
and once to find somewhere safe to hideaway 

It still needs lots of improvement
'''
import time
import random
import queue


MOVE_DIC = { 
		"none":0,
		"left":1,
		"right":2,
		"up":3,
		"down":4,
		"bomb":5
}
class agent:
	def __init__(self, player_num, env):
		self.name = "deep orange"
		self.player_num = player_num
		self.env = env
		self.reservedMoves = []



	def give_next_move(self, solid_state):
		'''
		This method is called each time the player needs to choose an 
		action

		solid_state: is a dictionary containing all the information about the board
		'''
		action = MOVE_DIC["none"] # just in case

		self.board = solid_state["board"] 
		self.done = solid_state["done"]
		self.bombs = solid_state["bombs"]
		self.turn = solid_state["turn"]
		self.player = solid_state["players"][self.player_num-1]
 
		(x,y) = self.player.position

		if (self.reservedMoves): #if we have already decided on what moves to play
			return self.reservedMoves.pop()


		tiles_in_range = self.get_tiles_in_range(solid_state) # dangerous tiles
		(x, y) = self.player.position
		if (self.player.position in tiles_in_range) or (self.board[x][y] >= 6) :#run away then
			self.reservedMoves = find_path_to_safe_cell(self,Node_cell(self.player.position, None, None), tiles_in_range, [], self.board)
			print(self.reservedMoves)
			if (not self.reservedMoves):
				print("I could not find an escape so I stand still")
				#sys.exit()
				action = (MOVE_DIC['none'])
			else:
				action = self.reservedMoves.pop()

		else:
			if (self.player.num_bombs < 1): #without this bot can jumpback into its explosion
				return MOVE_DIC["none"]
			current_node = Node_cell(self.player.position, None, None)
			for child in current_node.generate_children():
				if check_block_child(child.position,self.board):
					action = MOVE_DIC["bomb"]
					return action
			#else find a place to do it
			self.reservedMoves = find_path_next_to_block(self,Node_cell(self.player.position, None, None), tiles_in_range, [], self.board)
			if (not self.reservedMoves):
				print("I could not find a good block")
				action = (MOVE_DIC['none'])
			else:
				action  = self.reservedMoves.pop()

		return action

	def get_tiles_in_range(self, solid_state):
		'''
		get surrounding tiles impacted near bomb
		'''

		bombs = solid_state["bombs"]

		
		all_tiles_in_range = []
		for bo in bombs:
			all_tiles_in_range.append(bo.tiles_in_range)
		return all_tiles_in_range




class Node_cell:
	def __init__(self, curr_pos, parent,parent_move):
		self.position = curr_pos
		self.parent_move = parent_move
		self.children = [] # will be populated soon
		self.parent = parent

		

		#for child in possible_children: 
			#if check_legal_child(child.position, board) and child.position not in already_visited_cells:
				#self.children.append(child)
		#children are now populated for legal position.
	def generate_children(self):
		curr_pos = self.position
		tile_up = (curr_pos[0]-1,curr_pos[1])
		child_up = Node_cell(tile_up, self, MOVE_DIC["up"])
		tile_down = (curr_pos[0]+1,curr_pos[1])
		child_down = Node_cell(tile_down, self, MOVE_DIC["down"])
		tile_left = (curr_pos[0],curr_pos[1]-1)
		child_left = Node_cell(tile_left, self, MOVE_DIC["left"])
		tile_right = (curr_pos[0],curr_pos[1]+1)
		child_right = Node_cell(tile_right, self, MOVE_DIC["right"])
		
		return [child_up, child_down, child_left, child_right]


def check_legal_child( p_child, already_visited_cells,board):
	'''
	p_child is a tuple (x,y)
	'''
	(x, y) = p_child
	if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
		return False # if the child cell is out of range return false
	elif board[x][y] != 5 and board[x][y] != 0:
		return  False # if it is anything but a b or empty cell
	elif p_child in already_visited_cells: # child has been already generated
		return False
	else:
		return True

def check_block_child( p_child,board):
	'''
	returns true if the position has a block
	p_child is a tuple (x,y)
	'''
	(x, y) = p_child
	if x < 0 or x >= len(board) or y < 0 or y >= len(board[0]):
		return False # if the child cell is out of range return false
	elif board[x][y] == 3:
		return  True # if it is anything but a b or empty cell
	else:
		return False



def find_path_to_safe_cell(self,starting_node, unsafe_cells, already_visited_cells, board):
	answer = False
	already_visited_cells.append(starting_node.position)
	bfs_q = queue.Queue()
	for ch in starting_node.generate_children():
		if( check_legal_child(ch.position, already_visited_cells,board)):
			bfs_q.put(ch)
	safeNode = False
	while(not bfs_q.empty()):
		current_node = bfs_q.get()
		if ( current_node.position not in unsafe_cells[0]):
			safeNode = current_node
			break
		else:
			for child in current_node.generate_children():
				is_it_valid = check_legal_child(child.position, already_visited_cells,board)
				already_visited_cells.append(child.position)
				#print(is_it_valid)
				if ( is_it_valid):
					bfs_q.put(child)
	if ( safeNode):
		path_to_safe_cell = []
		tempNode = safeNode
		while(tempNode.parent_move):
			path_to_safe_cell.append(tempNode.parent_move)
			tempNode = tempNode.parent
		return path_to_safe_cell


	return False #if queue gets empty it means there is no solution



def find_path_next_to_block(self,starting_node, unsafe_cells, already_visited_cells, board):
	#print("looking at cell:",starting_node.position )
	answer = False
	bfs_q = queue.Queue()
	bfs_q.put(starting_node)
	goalNode = False
	while(not bfs_q.empty() and not goalNode):
		current_node = bfs_q.get()
		if ( current_node.position not in unsafe_cells):
			for child in current_node.generate_children():
				if check_block_child(child.position,board):
					goalNode = current_node
		for child in current_node.generate_children():
			is_it_valid = check_legal_child(child.position, already_visited_cells,board)
			already_visited_cells.append(child.position)
			print(is_it_valid)
			if ( is_it_valid):
				bfs_q.put(child)
		#print("bfs_q.qsize()",bfs_q.qsize())

	if ( goalNode):
		path_to_safe_cell = []
		tempNode = goalNode
		while(tempNode.parent_move):
			path_to_safe_cell.append(tempNode.parent_move)
			tempNode = tempNode.parent
		return path_to_safe_cell


	return False #if queue gets empty it means there is no solution
