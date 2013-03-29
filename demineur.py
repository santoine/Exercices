import random
import re

EMPTY = "0"
BOMB = "B"
FLAGGED = "F"
DISCOVERED = "D"
UNKNOWN = "?"
BASE = "X"

class GameConfiguration:
	"""Stores the configuration of the game, which are the size of the board and the number of mines"""
	def __init__(self, mines = 10, rows = 9, cols = 9):
		self.mines = mines
		self.rows = rows
		self.cols = cols	

class Element:
	"""Defines an element of the board"""
	content = EMPTY
	state = BASE
	
	def __init__(self, x, y):
		"""Intialise position in the game"""
		self.x = x
		self.y = y

	def print_element(self):
		"""Returns the content if the element is discovered, otherwise return the state"""
		if self.state == DISCOVERED:
			if self.content != "0":
				return self.content
			else :				
				return " "
		else :
			return self.state
		
class Board:
	"""The board contains all the data of the game"""
	def __init__(self, configuration=GameConfiguration()):
		self.configuration = configuration
		self.elements = self.generate_elements()
		self.populate_board()

	def generate_elements(self):
		"""returns a two sizes matrix filled with Element instances"""
		elements = []
		for x in range(0, self.configuration.rows):
			row = []
			for y in range(0, self.configuration.cols):
				col = Element(x,y)
				row.append(col)
			elements.append(row)	
		return elements

	def print_board(self):
		#print "".join(str(range(10))
		for row in self.elements:
			row_content = ""
			for element in row:
				row_content += element.print_element()+" "
			print row_content

	def populate_board(self):		
		self.addMines(self.configuration.mines)
		self.computeNumbersAroundMinePosition()		

	def addMines(self, numberOfMines):
		"""randomly adds mines on the board"""
		while numberOfMines > 0 :
			row_num = random.randint(0, self.configuration.rows - 1)
			col_num = random.randint(0, self.configuration.cols - 1)
			if self.elements[row_num][col_num].content == EMPTY:				
				self.elements[row_num][col_num].content = BOMB
				numberOfMines -= 1

	def computeNumbersAroundMinePosition(self):
		for row in self.elements:
			for element in row:
				if element.content == BOMB:
					bx = element.x - 1
					by = element.y - 1
					#print str(element.x) + ","+str(element.y)
					#Add one to mark the bomb around the element
					for x in range(bx, bx + 3):
						for y in range(by, by + 3):
							# Chechs that we are still in the board limits
							if x >= 0 and y >= 0 and x < self.configuration.rows and y < self.configuration.cols:
								# add one if the element is not a bomb
								if self.elements[x][y].content != BOMB:
									self.elements[x][y].content = str(int(self.elements[x][y].content) + 1)						

	def discover(self, x, y):
		""" Discovers the selected element and all the elements around"""
		element = self.elements[x][y]
		if element.state != FLAGGED and element.state != DISCOVERED:
			element.state = DISCOVERED
			if element.content == EMPTY:
				#recursively seach for other empty elements around
				bx = element.x - 1
				by = element.y - 1
				for x in range(bx, bx + 3):
					for y in range(by, by + 3):
						if x >= 0 and y >= 0 and x < self.configuration.rows and y < self.configuration.cols:
							#print "treat :"+ str(x) + ","+str(y)							
							self.discover(x,y)
			# 	# Recursively discovers the elements around him
			# 	for x in range(bx, bx + 3):
				# for y in range(by, by + 3):
				return True
			elif element.content == BOMB:
				return False
			else:
				# When a number do nothing
				return True

	def flag(self, x, y):
		""" Marks an element as flagged, if already flagged, unflag it"""
		if self.elements[x][y].state != FLAGGED:
			self.elements[x][y].state = FLAGGED
		else :
			self.elements[x][y].state = BASE

	def isGameWon(self):
		for row in self.elements:
			for element in row:
				if element.content == BOMB and element.state != FLAGGED:
					return False
		return True

def textGame():
	b = Board()
	b.print_board()
	end = False
	while not end:
		movement = raw_input("(D)iscover/(F)lag :")
		positions = re.split(',',raw_input("Position (like 0,0) : "))			
		x = int(positions[0])
		y = int(positions[1])

		res = True
		if movement == "D":
			res = b.discover(x,y)
		if movement == "F":
			b.flag(x,y)
		if not res:
			print "You loose!"
		end = b.isGameWon()
		b.print_board()

textGame()